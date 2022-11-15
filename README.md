# VIEWS API (v.0.3)

This repository documents the VIEWS API. It is written in `Python/FastAPI` and as such conforms to the OpenAPI standard. The API currently returns JSON, with all data currently being row-based and row-indexed (an array of observations, where each observation is its own array; not an array of columns).

The VIEWS API is available in _alpha_ testing mode at [https://api.viewsforecasting.org](https://api.viewsforecasting.org).

To learn more about the VIEWS API and its content, please visit the [wiki pages](https://github.com/prio-data/views_api/wiki/). 


## Fetching and downloading data from the API


### Step 1: Identify your dataset of interest

Please consult the [list of available datasets](https://github.com/prio-data/views_api/wiki/Available-datasets) in the wiki section to learn more about the available datasets, and the corresponding [codebooks](https://github.com/prio-data/views_api/wiki/Codebooks) to browse the variables they contain. 


### Step 2: Choose access method

There are multiple ways to fetch and download data from the VIEWS API. 

- **Option 1.** Make an API call using the instructions in the [wiki section](https://github.com/prio-data/views_api/wiki/Making-an-API-call). This will load the chosen dataset directly in your browser for further action. The URL can also be used to download the data as a csv file using *Option 2*. 

- **Option 2.** Specify an API call using the instructions in the [wiki section](https://github.com/prio-data/views_api/wiki/Making-an-API-call) and use our [helper notebook](https://github.com/prio-data/views_api/blob/master/DataExploration/Fetch%20and%20download%20data%20from%20the%20VIEWS%20API.ipynb) to fetch and download the selected data as a csv file.  

- **Option 3.** Use our [interactive data exploration tool](https://api.viewsforecasting.org/docs) to specify your API call and generate a URL that automatically downloads the data of interest as a csv file. 

## Questions?

Please contact [views@pcr.uu.se](mailto:views@pcr.uu.se).

