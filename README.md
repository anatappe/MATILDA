# MATILDA - Modeling water resources In glacierized catchments

The MATILDA model connects the HBV model (Bergström, 1986), a simple hydrological bucket model, which computes runoff and a simple DDM approach to compute the glacier melt. It may also be connected to the glacier mass balance model COSIPY (COupled Snow and Ice energy and MAss Balance in Python). The aim is to generate runoff projections under different climate scenarios and use the results to help planing future water management strategies in the modeled catchments. 

## Overview

MATILDA uses a modified version of the pypdd tool (https://github.com/juseg/pypdd.git) to calculate runoff from the glacier(s) with a simple DegreeDayModel approach and a modified version of the LHMP tool (https://github.com/hydrogo/LHMP.git) which translates the HBV model into python. It can run on input data from COSIPY, the translation of the COSIMA model into python (https://github.com/cryotools/cosipy.git).

### Requirements
Clone
```
Clone this repo to your local machine using https://github.com/anatappe/MATILDA.git
```

The tool should run with any Python3 version on any computer operating system. It was developed on Python 3.6.9 on Ubuntu 18.04.
It requires the following Python3 libraries:
- xarray
- numpy
- pandas
- matplotlib
- scipy
- os
- datetime

The MATILDA package and the necessary packages can be installed to you local machine by using pip. Just navigate into the cloned folder and use the following command:
```
pip install .
```

### Data

The necessary input a either a csv with a time series of temperature (°C), precipitation (mm) and if possible evapotranspiration (mm) data in the following format or the output netcdf and csv from the COSIPY model. A series of runoff observations (mm) are used to validate the model output.

| TIMESTAMP            | T2            | RRR            | PE            |
| -------------        | ------------- | -------------  | ------------- |
| 2011-01-01 00:00:00  | -18.2         | 0.00           | 0.00          |
| 2011-01-01 01:00:00  | -18.3         | 0.1            | 0.00          |
| 2011-01-01 02:00:00  | -18.2         | 0.1            | 0.00          |

| Date          | Qobs          |
| ------------- | ------------- |
| 2011-01-01    | 0.00          |
| 2011-01-01    | 0.00          |


It is also necessary to adjust the parameters of the DDM and the HBV model to the prevailing conditions in the test area. Since the DDM model calculates the glacier melt, it is necessary to scale the input data to the glacier. This can be done with a lapserate for temperature and precipitation and the height difference between the measurement station of the data and the glacier or with a DEM and glacier mask.

### Workflow

The MATILDA package consists of four different modules: DDM, HBV, plots and statistics which have different submodules for the individual steps. 
To use the whole package, the following steps are recommended:
- read in your data and define a spin up and simulation period
- if you only use a csv, define a lapse rate for temperature and precpitation and a height difference between your data and the mean glacier height to downscale your dataframe for the DDM
- define the output frequency (daily, weekly, monthly or yearly)
- use the DDM module to calculate the positive degree days and use the output dataset to run the DDM. Specify the degree day factors here
- run the HBV model with your dataframe. Adjust the parameters for the accordingly. If evapotranspiration is not available, it is calculated automatically
- merge the two output dataframe with your observations to calculate the Nash–Sutcliffe model efficiency coefficient and perform a simple statistical analysis with the tools from the stats module
- plot runoff, meteorological parameters and HBV output series with the plots module 

Example run
```
from MATILDA import DDM, HBV, stats, plots

working_directory = "...MATILDA/"
data_csv = "data_2010-2019.csv"
obs = "observations_2010_2019.csv"
output = working_directory + "Output/"

cal_period_start = '2010-01-01 00:00:00' # beginning of  period
cal_period_end = '2010-12-31 23:00:00' # end of period: one year is recommended
sim_period_start = '2011-01-01 00:00:00' # beginning of simulation period
sim_period_end = '2019-12-31 23:00:00'

lapse_rate_temperature = -0.006 # K/m
lapse_rate_precipitation = 0
height_diff = 21 # height difference between AWS (4025) and glacier (4036) in m

cal_exclude = False # Include or exclude the calibration period
plot_frequency = "Weekly" # possible options are Daily, Weekly, Monthly or Yearly
plot_save = True # saves plot in folder, otherwise just shows it in Python

## Data input preprocessing
print('---')
print('Starting MATILDA model run')
print('Read input csv file %s' % (data_csv))
print('Read observation data %s' % (observation_data))
df = pd.read_csv(working_directory + data_csv)
obs = pd.read_csv(working_directory + observation_data)

print("Spin up period between " + str(cal_period_start) + " and "  + str(cal_period_end))
print("Simulation period between " + str(sim_period_start) + " and "  + str(sim_period_end))
# Downscaling the dataframe to the glacier height
df_DDM = df.copy()
df_DDM["T2"] = df_DDM["T2"] + height_diff * float(lapse_rate_temperature)
df_DDM["RRR"] = df_DDM["RRR"] + height_diff * float(lapse_rate_precipitation)

## DDM model
print("Running the degree day model")
# Calculating the positive degree days
degreedays_ds = DDM.calculate_PDD(ds) # include either downscaled glacier dataframe or dataset with mask
# Calculating runoff and melt
output_DDM = DDM.calculate_glaciermelt(degreedays_ds) # output in mm, parameter adjustment possible

## HBV model
print("Running the HBV model")
# Runoff calculations for the catchment with the HBV model
output_hbv = HBV.hbv_simulation(df, cal_period_start, cal_period_end) # output in mm, individual parameters can be set here

## Output postprocessing
output = pd.concat([output_hbv, output_DDM], axis=1)
output = pd.concat([output, obs], axis=1)
output["Q_Total"] = output["Q_HBV"] + output["Q_DDM"]

nash_sut = stats.NS(output["Qobs"], output["Q_Total"]) # Nash–Sutcliffe model efficiency coefficient
print("The Nash–Sutcliffe model efficiency coefficient of the total model is " + str(round(nash_sut, 2)))

print("Writing the output csv to disc")
output = output.fillna(0)
output.to_csv(output_path + "model_output_" +str(cal_period_start[:4])+"-"+str(sim_period_end[:4]+".csv"))

## Statistical analysis
# Daily, monthly or yearly output
if plot_frequency == "Daily":
    plot_data = output_calibration.copy()
elif plot_frequency == "Weekly":
    plot_data = output_calibration.resample("W").agg(
        {"T2": "mean", "RRR": "sum", "PE": "sum", "Q_HBV": "sum", "Qobs": "sum", \
         "Q_DDM": "sum", "Q_Total": "sum", "HBV_AET": "sum", "HBV_snowpack": "mean", \
         "HBV_soil_moisture": "mean", "HBV_upper_gw": "mean", "HBV_lower_gw": "mean"})
elif plot_frequency == "Monthly":
    plot_data = output_calibration.resample("M").agg(
        {"T2": "mean", "RRR": "sum", "PE": "sum", "Q_HBV": "sum", "Qobs": "sum", \
         "Q_DDM": "sum", "Q_Total": "sum", "HBV_AET": "sum", "HBV_snowpack": "mean", \
         "HBV_soil_moisture": "mean", "HBV_upper_gw": "mean", "HBV_lower_gw": "mean"})
elif plot_frequency == "Yearly":
    plot_data = output_calibration.resample("Y").agg(
        {"T2": "mean", "RRR": "sum", "PE": "sum", "Q_HBV": "sum", "Qobs": "sum", \
         "Q_DDM": "sum", "Q_Total": "sum", "HBV_AET": "sum", "HBV_snowpack": "mean", \
         "HBV_soil_moisture": "mean", "HBV_upper_gw": "mean", "HBV_lower_gw": "mean"})

stats_output = stats.create_statistics(output_calibration)
stats_output.to_csv(output_path + "model_stats_" +str(output_calibration.index.values[1])[:4]+"-"+str(output_calibration.index.values[-1])[:4]+".csv")


## Plotting the output data
# Plot the meteorological data
fig = plots.plot_meteo(plot_data, plot_frequency)
if plot_save == False:
	plt.show()
else:
	plt.savefig(output_path + "meteorological_data_"+str(plot_data.index.values[1])[:4]+"-"+str(plot_data.index.values[-1])[:4]+".png")

# Plot the runoff data
fig1 = plots.plot_runoff(plot_data, plot_frequency, nash_sut)
if plot_save == False:
	plt.show()
else:
	plt.savefig(output_path + "model_runoff_"+str(plot_data.index.values[1])[:4]+"-"+str(plot_data.index.values[-1])[:4]+".png")

# Plot the HBV paramters
fig2 = plots.plot_hbv(plot_data, plot_frequency)
if plot_save == False:
	plt.show()
else:
	plt.savefig(output_path + "HBV_output_"+str(plot_data.index.values[1])[:4]+"-"+str(plot_data.index.values[-1])[:4]+".png")

print('Saved plots of meteorological and runoff data to disc')
print("End of model run")
print('---')
```


## Built With
* [Python](https://www.python.org) - Python
* [COSIPY](https://github.com/cryotools/cosipy.git) - COupled Snow and Ice energy and MAss Balance in Python
* [pypdd](ttps://github.com/juseg/pypdd.git) - Python positive degree day model for glacier surface mass balance
* [LHMB](https://rometools.github.io/rome/) - Lumped Hydrological Models Playgroud - HBV Model

## Authors

* **Phillip Schuster** - *Initial work* - (https://github.com/anatappe)
* **Ana-Lena Tappe** - *Initial work* - (https://scm.cms.hu-berlin.de/tappelen)


See also the list of [contributors](https://scm.cms.hu-berlin.de/sneidecy/centralasiawaterresources/-/graphs/master) who participated in this project.

## License

This project is licensed under the HU Berlin License - see the [LICENSE.md](LICENSE.md) file for details

### References

For COSIPY:
	•	Sauter, T. & Arndt, A (2020). COSIPY – An open-source coupled snowpack and ice surface energy and mass balance model. https://doi.org/10.5194/gmd-2020-21

For PyPDD:
	•	Seguinot, J. (2019). PyPDD: a positive degree day model for glacier surface mass balance (Version v0.3.1). Zenodo. http://doi.org/10.5281/zenodo.3467639

For LHMP and HBV:
	•	Ayzel, G. (2016). Lumped Hydrological Models Playground. github.com/hydrogo/LHMP, hub.docker.com/r/hydrogo/lhmp/, doi: 10.5281/zenodo.59680.
	•	Ayzel G. (2016). LHMP: lumped hydrological modelling playground. Zenodo. doi: 10.5281/zenodo.59501.
	•	Bergström, S. (1992). The HBV model: Its structure and applications. Swedish Meteorological and Hydrological Institute.
