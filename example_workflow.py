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

plot_frequency = "M" # possible options are "D" (daily), "W" (weekly), "M" (monthly) or "Y" (yearly)
plot_frequency_long = "Monthly" # Daily, Weekly, Monthly or Yearly

## Data input preprocessing
df = pd.read_csv(working_directory + data_csv)
obs = pd.read_csv(working_directory + observation_data)

# Downscaling the dataframe to the glacier height
df_DDM = df.copy()
df_DDM["T2"] = df_DDM["T2"] + height_diff * float(lapse_rate_temperature)
df_DDM["RRR"] = df_DDM["RRR"] + height_diff * float(lapse_rate_precipitation)

# Calculating the positive degree days
degreedays_ds = DDM.calculate_PDD(df_DDM)
# include either downscaled glacier dataframe or dataset with mask
# Calculating runoff and melt
output_DDM = DDM.calculate_glaciermelt(degreedays_ds) # output in mm, parameter adjustment possible

## HBV model
# Runoff calculations for the catchment with the HBV model
output_hbv = HBV.hbv_simulation(df, cal_period_start, cal_period_end) # output in mm, individual parameters can be set here

## Output postprocessing
output = pd.concat([output_hbv, output_DDM], axis=1)
output = pd.concat([output, obs], axis=1)
output["Q_Total"] = output["Q_HBV"] + output["Q_DDM"]

nash_sut = stats.NS(output["Qobs"], output["Q_Total"]) # Nash–Sutcliffe model efficiency coefficient

output.to_csv(output_path + "model_output_" +str(cal_period_start[:4])+"-"+str(sim_period_end[:4]+".csv"))

## Statistical analysis
# Daily, weekly, monthly or yearly output
plot_data = output_calibration.resample(plot_frequency).agg(
    {"T2": "mean", "RRR": "sum", "PE": "sum", "Q_HBV": "sum", "Qobs": "sum", \
    "Q_DDM": "sum", "Q_Total": "sum", "HBV_AET": "sum", "HBV_snowpack": "mean", \
    "HBV_soil_moisture": "mean", "HBV_upper_gw": "mean", "HBV_lower_gw": "mean"})
plot_data = plot_data[cal_period_start: sim_period_end]

stats_output = stats.create_statistics(output_calibration)
stats_output.to_csv(output_path + "model_stats_" +str(output_calibration.index.values[1])[:4]+"-"+str(output_calibration.index.values[-1])[:4]+".csv")

## Plotting the output data
# Plot the meteorological data
fig = plots.plot_meteo(plot_data, plot_frequency_long)
plt.show()

# Plot the runoff data
fig1 = plots.plot_runoff(plot_data, plot_frequency_long, nash_sut)
plt.show()

# Plot the HBV paramters
fig2 = plots.plot_hbv(plot_data, plot_frequency_long)
plt.show()
