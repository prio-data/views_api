# VIEWS API (v.0.3)

This repository documents the VIEWS API. It is written in `Python/FastAPI` and as such conforms to the OpenAPI standard. The API currently returns JSON, with all data currently being row-based and row-indexed (an array of observations, where each observation is its own array; not an array of columns).

The VIEWS API is available in _alpha_ testing mode at [https://api.viewsforecasting.org](https://api.viewsforecasting.org).

For assistance in exploring the VIEWS data available via the API, please see the user guide below, visit the self-documenting and exploratory interface at [https://api.viewsforecasting.org/docs](https://api.viewsforecasting.org/docs), or use the example resources in the `Tools` folder.

**Questions?** Please contact [views@pcr.uu.se](mailto:views@pcr.uu.se).


## Making an API call

The general form of the api call is:

`https://api.viewsforecasting.org/{run}/{loa}/[{type_of_violence}/[{variable}]]?filters`, where

- `/{run}`: The `run_id` for fetching forecasts. There should be a `current` run which defaults to the most recent data release. You may also choose `run_id` in the conventional format `{model name}{model version}_{production run}_{try sequence}`, where

  - `model name` is a a short label for the prediction model at hand, e.g. the **fatalities** model that is currently in production. To learn more about current and deprecated VIEWS models, please visit https://viewsforecasting.org/methodology.

  - `model version` is a numeric identifier that specifies the concerned version of the aforementioned model, e.g. `001` (from 2022 onwards). Changes to the model(s) in production (such as new ensembling techniques or updates to model compositions) are implemented in batches and documented in the [model changelog](https://github.com/prio-data/viewsforecasting/blob/main/CHANGELOG.md). Each batch of changes prompts a new model version, upon which the corresponding numeric identifier is incremented by 1.

  - `production run` specifies the data release from the aforementioned model and model version. From 2022 onwards, all production runs in ViEWS are named by means of the calendar year (`YYYY`) and calendar month (`MM`) of the last data that informs a given run, e.g. `2022_07`. Prior to 2022, the production runs were named in accordance with the year and month of the data release at hand.

  - `try sequence` indicates whether the aforementioned production run required any bug fixes prior to successful completion. If the production run was completed on the first attempt, the try counter is given the default value of `t01` (`01` prior to 2022). For each additional attempt, the counter is incremented by 1. Errors and resolutions are documented in the model changelog.

- `/{loa}`: The level of analysis (`cm` for country-month, `pgm` for PRIO-GRID-month). Please consult VIEWS' [definitions](https://viewsforecasting.org/methodology/definitions) for further details.

- `/{type_of_violence}`: The type of violence for which you want forecasts (state-based conflict (`sb`), non-state conflict (`ns`), or one-sided violence (`os`); see our [definitions](https://viewsforecasting.org/methodology/definitions) for more information). Some API nodes contain data from **predictors**, i.e. individual features informing the forecasts. They can be obtained by using the (`px`) node at this level.

- `/{variable}`: The model or variable of interest. See the codebook for each dataset at https://api.viewsforecasting.org/{run}/codebook for a list of available variables. 

- `/{partition}`: The partition of data to retrieve (`predict`, `eval` or `calib`), see the [data partitions](https://viewsforecasting.org/methodology/definitions description on our website for more information.

For example, [https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb/sc_cm_sb_main] will return the following things:

1. A set of `metadata` objects, containing:

- A paging breadcrumb, containing a `next_page` and `prev_page` URL, that allow you to easily access the whole retrieved dataset page-by-page. Following these "next" and "previous" URL links will allow you to access the dataset with ease.

- Paging information, containing the total number of pages (`page_count`), rows (`row_count`), pages (`page_count`), as well as the current page (`page_cur`) you are exploring.

- `model_tree` : A model tree describing the relations of the models you have selected and will receive output from. Models can be ensembles of other models, and, similarly, can be components of ensembles, arbitrarily nested. This allows you to explore ensembles and components with relative ease (for examle, `sc_cm_sb_main` is composed of a set of models as a parent).

- `models`: A model set (presented as an array) - a list of all the models from which output will be retrieved by the API call.

2. A `data` matrix containing calendar `year`, calendar `month`, identifiers for the chosen level of analysis (`country_id/name/ISO`, `priogrid`, see all filters below) and the values for each of the predictions or data points for the given period.


### Retrieving multiple models

The API does not require you to go full depth. For example, if you call `https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm`, you will get all the models at the `country-month` level of analysis for all available types of violence.

Similarly, if you call `https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb` you will get output from all models that predict state-based violence.

Note that the order matters, it's always `{loa}/{type_of_violence}/{model}`.

All filtering works at all levels.


### Filters

All filters are treated as `AND`, with the exception of repeating the same filter key, which, where allowed (see below), will be treated as `OR`. This conforms to the OpenAPI standard. All filters are designed to 'fail-safe', i.e. if a filter is wrongly specified or does not exist, it is simply ignored.

**1. Spatial filters:**

  - `iso`: An ISO country code in 3-letter format (e.g. `JPN`). A list is allowed by repeating the key, which will then be treated as `OR` (e.g. `iso=JPN&iso=CHN` will retrieve data for both China and Japan).

  - `country_id`: A VIEWS-specific country ID in integer form (e.g. `237`). A list is allowed by repeating the key, which will be treated as `OR` (e.g. `country_id=47&country_id=50` will retrieve data for both Burkina Faso and Mali). A matrix of the VIEWS country IDs with corresponding country names and gwcodes can be downloaded from the [resource page](https://viewsforecasting.org/resources/#downloads) on our website.

  - `gwcode`: A country ID from the [Gleditsch & Ward (1999)](https://doi.org/10.1080/03050629908434958) system membership list. A list is allowed by repeating the key, which will be treated as `OR`, shown by the examples above.

  - `priogrid`: A list of PRIO-GRID grid cell identifiers (see our [definitions](https://viewsforecasting.org/methodology/definitions)). A list is allowed by repeating the key, which will be treated as `OR`, shown by the examples above.

  - `lat` + `lon`: A pair of latitudes and longitudes, for which data will be retrieved. Both need to be supplied.

  - `lat_ne` + `lon_ne` + `lat_sw` + `lon_sw`: A bounding box for which to retrieve the data. The filter will retrieve data from lat_ne/lon_ne + lat_sw/lon_sw. Both need to be supplied.

All spatial filters work for both PRIO-GRID and country levels, and are cast appropriately. E.g., if you specify a country filter for PRIO-GRID predictions, you will be given PRIO-GRID predictions for all grid cells located in that country. Country allocation is determined by PRIO-GRID 2.0 procedures (see the PRIO-GRID 2.0 codebook), by which they draw upon the country delimitations from the cShapes dataset v.0.4-2 and assign grid cells to the country that covers the largest share of a given cell's area ([see the PRIO-GRID 2.0 codebook, p. 13](https://grid.prio.org/extensions/PRIO-GRID-Codebook.pdf))

Please note that all latitude and longitude pairs must be supplied in decimal degree format (DD) (+ for the northern and eastern hemisphere, - for the southern and western), using the dot as the decimal separator. A latitude of 77 degrees, 30 minutes and 30 seconds South should e.g. be entered as -77.508333. A DDM or DMS converter can be added if such is needed. Conversions from projected coordinate systems may also be added in future versions if such are desirable, and reverse projection algorithms are available.

Concatenating **different filters** in this class will be treated as `AND`, and are thus  meaningless. For example, a call for https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb?iso=EGY&gwcode=615 will be translated as `iso=EGY AND gwno=615`, i.e. an attempted retrieval of all rows for Egypt-Algeria and thus resulting in zero data.

Concatenating **identical filters** in the same class will be treated as `OR`. https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb?iso=EGY&iso=DZA will be translated as `iso=EGY` `OR` `iso=DZA`, i.e. retrieve all rows that relate EITHER to Egypt or Algeria.

**2. Temporal filters:**

  - `date_start`: An ISO date in the format `YYYY-MM-DD` for the first month to be retrieved. If not specified, `date_start` will default to the first date in the dataset.

  - `date_end`: An ISO date in the format `YYYY-MM-DD` for the last month to be retrieved. If not specified, `date_end` will default to the last date in the dataset.

  - `month`: A VIEWS `month_id`, i.e. a sequence starting from 1 that increments by one for each month, where `month_id=1` is January 1980. `month` can also be specified as a list by repeating the parameter (e.g. `&month=401&month=403`). This will be treated as `OR`, and will retrieve both month 401 and 403, i.e. May 2013 and July 2013).

Mixing the three parameters above will be interpreted as `AND`, i.e. `date_end=2019-01-01 AND date_end=2020-12-31` will retrieve all predictions for 2019 and 2020. Note that the day part (`DD`, 1-31) is ignored and always treated as 1 for `date_start`, and 28/29/30/31 for all `date_end`, so as to include full months (VIEWS operates on a monthly resolution).

**3. Steps and data filters:**

  - `data`: If omitted (or set to `True`), it will retrieve the data object. If not omitted, it will only retrieve metadata (model list and model tree).

  - For advanced use, a `steps` boolean parameter is given. Only use this if you fully understand the VIEWS methodology and need the individual steps. Due to large data sizes, also reduce the pagesize for best results. Note that this flag only makes sense if `data=True` and has no effect for dynamically simulated (dynasim/ds) models or similar.


**4. Paging and keys:**

TBC


### Example Queries:

https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm?iso=egy&month=501: Fetch all country-month predictions (for all types of violence) for Egypt, for `month` 501 (September 2021). Page 1 will be retrieved.

https://api.viewsforecasting.org/fatalities001_2022_07_t01/pgm/sb?iso=dza&month=501&month=502&pagesize=10: Fetch all PRIO-GRID-month predictions for state-based conflict in Algeria for `month` 501 and 502 (September-October 2021). Page 1 will be retrieved.

https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb?lat=20&lon=15&month=501 : Fetch all country-month predictions for state-based conflict for the country located at `latitude=20` and `longitude=15` for  `month=501` (September 2021).

https://api.viewsforecasting.org/fatalities001_2022_07_t01/cm/sb/sc_cm_sb_main?lat_ne=25&lon_ne=30&lat_sw=30&lon_sw=10&month=500: Fetch all country-level predictions for state-based conflict from the main ensemble model, for all countries located in a square bounded by 25N30E and 30S10W, for `month=500`.

https://api.viewsforecasting.org/fatalities001_2022_07_t01/pgm?iso=PAL&date_start=2010-01-01&date_end=2030-01-01: Fetch all PRIO-GRID-month predictions for Palestine between 2020-01-01 and 2030-01-01.

### Metadata

All datasets include some human readable metadata under the `codebook/` right below the model path (e.g. `https://api.viewsforecasting.org/fatalities001_2022_07_t01/codebook`).

### Further Reading:

You can use an interactive query manipulation tool (as well as look at the technical documentation) at https://api.viewsforecasting.org/docs/, or use the Jupyter notebook in the `Tools` folder.
