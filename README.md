# MATILDA - Modeling Water Resources in Glacierized Catchments

The MATILDA framework combines a simple positive degree-day routine (DDM) for computing glacier melt with the simple hydrological bucket model HBV (Bergström, 1986). Optionally, it can also be used with the glacier energy and mass balance model COSIPY (COupled Snow and Ice energy and MAss Balance in Python) instead of or alongside the DDM. The aim is to provide an easy-access open-source tool to assess the characteristics of small and medium-sized glacierized catchments and enable useres to estimate their future water resources for different climate change scenarios.
MATILDA is an ongoing project and therefore a work in progress.

## Overview

In the basic setup, MATILDA uses a modified version of the pypdd tool (https://github.com/juseg/pypdd.git) to calculate runoff from the glacier(s) with a simple positive degree-day model approach and a modified version of the LHMP tool (https://github.com/hydrogo/LHMP.git). Alternatively, the glacial melt can be calculated using COSIPY (https://github.com/cryotools/cosipy.git) while when using both glacier routines a comparison is provided. The comprehensive output contains the modeled time series for various components of the water balance, basic statistics of these variables, the Nash-Sutcliffe efficiency coefficient to evaluate the predictive skills of the model, and several plots of in- and output data.

![](MATILDA_overview.png)

### Requirements

Clone this repo to your local machine using https://github.com/anatappe/MATILDA.git


The tool should run with any Python3 version on any computer operating system. It was developed on Python 3.6.9 on Ubuntu 18.04.
It requires the following Python3 libraries:
- xarray
- numpy
- pandas
- matplotlib
- scipy
- os
- datetime

The MATILDA package and the necessary packages can be installed to you local machine by using pip. Just navigate into the cloned folder and use the following command
```
pip install .
```
or install the package directly from the source by using

```
pip install git+https://git@github.com/anatappe/MATILDA.git

```
### Data

The minimum input is a CSV-file containing timeseries of air temperature (°C), total precipitation (mm) and (if available) evapotranspiration (mm) data in the  format shown below. Alternatively, the model can be run on an input or output NetCDF-file, or input CSV-file of the COSIPY model. A series of runoff observations (mm) is used to validate the model output. At least daily data is required.

| TIMESTAMP            | T2            | RRR            | PE            |
| -------------        | ------------- | -------------  | ------------- |
| 2011-01-01 00:00:00  | -18.2         | 0.00           | 0.00          |
| 2011-01-01 01:00:00  | -18.3         | 0.1            | 0.00          |
| 2011-01-01 02:00:00  | -18.2         | 0.1            | 0.00          |

| Date          | Qobs          |
| ------------- | ------------- |
| 2011-01-01    | 0.00          |
| 2011-01-01    | 0.00          |


It is also necessary to adjust the parameters of the DDM and the HBV model to the prevailing conditions in the model area. Since the DDM model calculates the glacier melt, it is necessary to scale the input data to the glacier. In the most simple manner, this can be achieved by using a lapse rate for temperature and precipitation and the elevation difference between the reference altitudes of the data and the glacier. Alternatively, a digital elevation model (DEM) and a glacier mask can be provided to MATILDA to derive the necessary elevation values automatically.

### Workflow

The MATILDA package consists of four different modules: DDM, HBV, plots, and statistics which have different submodules for the individual steps. 
To use the whole package, the following steps are recommended:
- Read your data and define a spin-up and simulation period.
- If you only use a CSV, define a lapse rate for temperature and precpitation and an elevation difference between your data reference altitude and the mean glacier altitude to downscale your dataframe for the DDM.
- Define the output frequency (daily, weekly, monthly or yearly).
- Use the DDM module to calculate the positive degree days and use the output dataset to run the DDM. Specify the degree day factors and lapse rates here.
- Run the HBV model with your dataframe. Adjust the parameters for the accordingly. If evapotranspiration is not available, it is calculated automatically.
- Merge the two output dataframe with your observations to calculate the Nash–Sutcliffe model efficiency coefficient and perform a simple statistical analysis using the tools from the stats module.
- Plot runoff, meteorological parameters, and HBV output series using the plots module. 

An example script for the workflow can be found [here](example_workflow.py).

## Built using
* [Python](https://www.python.org) - Python
* [COSIPY](https://github.com/cryotools/cosipy.git) - COupled Snow and Ice energy and MAss Balance in Python
* [pypdd](https://github.com/juseg/pypdd.git) - Python positive degree day model for glacier surface mass balance
* [LHMB](https://rometools.github.io/rome/) - Lumped Hydrological Models Playgroud - HBV Model

## Authors

* **Phillip Schuster** - *Initial work* - (https://github.com/phiscu)
* **Ana-Lena Tappe** - *Initial work* - (https://github.com/anatappe)


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
