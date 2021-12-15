# API specification
# Version 0.3

### General

The current API is in _alpha_ testing mode, and a testing example is available at [https://api.viewsforecasting.org/].

The API is written in `Python/FastAPI` and as such conforms to the OpenAPI standard. The API self-documents itself (and exposes an exploratory interface) here: `https://api.viewsforecasting.org/docs`

The API currently returns JSON, with all data currently being row-based and row-indexed (an array of observations, where each observation is its own array; not an array of columns).

### Models

The general form of the api call is:

`address/run/{loa}/[{type_of_violence}/[{model}]]?filters`

where the following address is the 

- `/{run}` : The runid for fetching forecasts. There should be a `current` run, otherwise, a run id in the conventional format (e.g. `d_2021_02_01`).

- `/{loa}` : The level of analysis (`cm` for country-month, `pgm` for priogrid-month)

- `/{type_of_violence}` : The type of violence for which you want forecasts (`sb`, `ns`, `os`). Some API nodes contain **predictors**, i.e. features used to make forecasts. You obtain those by using the (`px`) node at this level.

- `/{model}` : The model name itself.

- `/{partition}` : The partition of data to retrieve (`predict`, `eval` or `calib`)

For example:

https://api.viewsforecasting.org/d_2021_02_01/cm/sb/cm_sb_main

will return the following things: 

1. a set of `metadata` objects, containing:

- A paging breadcrumb, containing a `next_page` and `prev_page` URL, that allow you to easily access the whole retrieved dataset page-by-page. Following these "next" and "previous" URL links will allow you to access the dataset with ease.

- Paging information, containing the total number of pages (`page_count`), rows (`row_count`), pages (`page_count`), as well as the current page (`page_cur`) you are exploring.

- `model_tree` : A model tree describing the relations of the models you have selected. Models can be ensembles of other models, and, similarly, can be components of ensembles, arbitrarily nested. This allows you to explore ensembles and components with relative ease (for examle, cm_sb_main is composed of a set of models as a parent).

- `models` : A model set (presented as an array) - a list of all the models that will be retrieved by the API call.

2. a `data` matrix containing `months`, `loa_ids` (`country_id/name/ISO`, `pg_id`) and the values of each of the predictions for the given month.


### Retrieving multiple models

The API does not require you to go full depth. For example, if you call:

https://api.viewsforecasting.org/d_2021_02_01/cm/

You will get all the models at the `country-month` level of analysis for all types of violence (sb, ns and os). Similarly, if you call: 

https://api.viewsforecasting.org/d_2021_02_01/cm/sb

You will get all the models predicting state-based violence.

Note that the order matters, it's always `level_of_analysis/type_of_violence/model`

All filtering works at all levels.

### Filters:

All filters are treated as 'AND', with the exception of repeating the same filter key, which, where allowed (see below), will be treated as OR. This conforms to the OpenAPI standard. All filters are designed to 'fail-safe', i.e. if a filter is wrongly specified or does not exist, it is simply ignored.

1. Spatial:

    - `iso` : An ISO country code, in 3-letter format (e.g. JPN). A list is allowed by repeating the key, which will then be treated as OR (e.g. iso=JPN&iso=CHN will retrieve data for both China and Japan).
    - `countryid`: ViEWS country id. A list is allowed by repeating the key, which will be treated as OR
    - `gwcode` : A Gleditsch and Ward country id. A list is allowed by repeating the key, which will be treated as OR.
    - `priogrid`: A list of Priogrid gids. A list is allowed by repeating the key, which will be treated as OR
    - `lat` + `lon`: A pair of latitudes and longitudes, for which data will be retrieved. Both need to be supplied.
    - `lat_ne` + `lon_ne` + `lat_sw` + `lon_sw`: A bounding box for which to retrieve the data. The filter will retrieve data from lat_ne/lon_ne + lat_sw/lon_sw. Both need to be

All spatial filters work for both priogrid and country levels, and are cast appropriately, e.g. if you specify a country filter for priogrid predictions, you will be given priogrid predictions for all those priogrid cells located in that country. Casting between lat/lon, priogrid and country is done per Priogrid rules (i.e. majority assignment rules). Similarly, if you specify a priogrid cell or a latitude/longitude pair. 

All latitude and longitude pairs are to be supplied in decimal degree format (DD) (+ for the northern and eastern hemisphere, - for the southern and western), using the dot as the decimal separator. For example, a latitude of 77 degrees, 30 minutes, 30 seconds South should be entered as -77.508333. A DDM or DMS converter can be added if such is needed. Conversions from projected coordinate systems may also be added in future versions if such are desirable, and reverse projection algorithms are available.

Concatenating **different filters** in this class will be treated as AND, and thus are meaningless. For example doing https://api.viewsforecasting.org/d_2021_02_01/cm/sb?iso=EGY&gwcode=615 will be translated in "iso = EGY AND gwno=615", i.e. retrieve all those rows that are in BOTH Egypt and Algeria. It will thus retrieve zero data.

Concatenating **identical filters** in the same class will be treated as OR. https://api.viewsforecasting.org/d_2021_02_01/cm/sb?iso=EGY&iso=DZA will be translated in "iso = EGY OR iso=DZA", i.e. retrieve all those rows that are EITHER in Egypt or Algeria.

2. Temporal 
    - `date_start` : An ISO date in the format YYYY-MM-DD for the first month to be retrieved. If not specified, will default to the first date in the dataset.
    - `date_end` : An ISO date in the format YYYY-MM-DD for the last month to be retrieved. If not specified will default to the last date in the dataset.
    - `month` : A ViEWS month_id, i.e. a sequence starting from 1, and incrementing for each month, where 1 is January of 1980. Can also be specified as a list by repeating the parameter (e.g. &month=401&month=403). This will be treated as OR, and will retrieve BOTH month 401 and 403, ie May 2013 and July 2013).

Mixing the three parameters will be interpreted as `AND`, i.e. `date_end=2019-01-01 AND date_end=2020-12-31` will retrieve all predictions for 2019 and 2020. Note that the day part (1-31) is ignored, and always treated as 1 for date_start and 28/29/30/31 for all date_end, as to include full months (as ViEWS operates on a monthly resolution).

3. Steps and data:
    - `data` : If omitted (or set to True), will retrieve the data object. If not omitted, will only retrieve metadata (model list and model tree).
    - For advanced use, a `steps` boolean parameter is given. Only use if you fully understand the ViEWS methodology and need the individual steps. Due to large datasizes, reduce the pagesize forbest results. Note that this flag only makes sense if data = True and has no effect fordinamically simulated (dynasim/ds) models or similar.


4. Paging and keys:
    - `pagesize` : You can specify a custom pagesize for how many rows are retrieved in a data page. Any value between 1 -- 10000 is acceptable. Useful for testing and debugging your code, when you do not want large amounts of data to be retrieved at each call. Not using this filter will use the default page-size of 1000.
    - `page` : Which page you want to retrieve. Pages beyond the last page will result in an empty data field. Not using this filter will retrieve page 1 (the first page). You can use the URL breadcrumb system or the paging system to then retrieve the next pages.
    - The API is currently fully open.

### Example Queries:

https://api.viewsforecasting.org/d_2021_02_01/cm?iso=egy&month=501 : Fetch all Country-Month predictions (state-based, non-state, one-sided) for Egypt, for month 501 (September 2021). Page 1 will be retrieved.

https://api.viewsforecasting.org/d_2021_02_01/pgm/sb?iso=dza&month=500&month=501&pagesize=10 : Fetch all state-based PrioGrid month predictions for Algeria for Months 501 and 502 (September + October 2021). Page 1 will be retrieved.

https://api.viewsforecasting.org/d_2021_02_01/cm/ns?lat=20&lon=15&month=501 : Fetch all Non-state predictions at country month for the country located at latitude=20 and longitude=15 for month 501 (September 2021) 

https://api.viewsforecasting.org/d_2021_02_01/cm/sb/cm_sb_main?lat_ne=25&lon_ne=30&lat_sw=30&lon_sw=10&month=500 : Fetch all state-based country-level predictions for the main ensemble model for those countries located in a square bounded by 25N30E and 10S10E.

https://api.viewsforecasting.org/d_2021_02_01/pgm?iso=PAL&date_start=2010-01-01&date_end=2030-01-01: Fetch all PrioGrid based predictions for Palestine between 2020-01-01 and 2030-01-01.

### Metadata

All models expose some human readable metadata under the `codebook/` right below the model path:

https://api.viewsforecasting.org/escwa_2021_05_01/codebook

### Further Reading:

You can use an interactive query manipulation tool (as well as look at the technical documentation) here:
https://api.viewsforecasting.org/docs/

Or you can use the attached notebook.
