# MATILDA - Modeling wATer resources In gLacierizeD cAtchments

The MATILDA model connects the HBV model (Bergström, 1986), a simple hydrological bucket model, which computes runoff and a simple DDM approach to compute the glacier melt. It may also be connected to the glacier mass balance model COSIPY (COupled Snow and Ice energy and MAss Balance in Python). The aim is to generate runoff projections under different climate scenarios and use the results to help planing future water management strategies in the modeled catchments. 

## Overview

MATILDA uses a modified version of the pypdd tool (https://github.com/juseg/pypdd.git) to calculate runoff from the glacier(s) with a simple DegreeDayModel approach and a modified version of the LHMP tool (https://github.com/hydrogo/LHMP.git) which translates the HBV model into python. It can run on input data from COSIPY, the translation of the COSIMA model into python (https://github.com/cryotools/cosipy.git).

### Requirements

Clone
```
Clone this repo to your local machine using https://scm.cms.hu-berlin.de/sneidecy/centralasiawaterresources.git
```

The tool should run with any Python3 version on any computer operating system. It was developed on Python 3.6.9 on Ubuntu 18.04.
It requires the following Python3 libraries:
- 	xarray
- 	numpy
- 	pandas
- 	matplotlib
-   scipy
-   os
-   datetime


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


## Built With
* [Python](https://www.python.org) - Python
* [COSIPY](https://github.com/cryotools/cosipy.git) - COupled Snow and Ice energy and MAss Balance in Python
* [pypdd](ttps://github.com/juseg/pypdd.git) - Python positive degree day model for glacier surface mass balance
* [LHMB](https://rometools.github.io/rome/) - Lumped Hydrological Models Playgroud - HBV Model

## Authors

* **Phillip Schuster** - *Initial work* - (https://scm.cms.hu-berlin.de/schustep)
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
