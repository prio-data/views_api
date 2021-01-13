from fastapi import FastAPI, APIRouter, Query
from starlette.requests import Request
from enum import Enum
from typing import Optional, List
from libdb import DBModel
from libdb.ViEWSModel import ModelTV, ModelLOA, simpleFactory
from libdb.APIConfig import Paging
from copy import deepcopy


app = FastAPI()
vRuns = DBModel.Runs()

AllModels = Enum('AllModels', {i: i for i in vRuns.dirty_full_model_list()})
AvailableRuns = Enum('AvailableRuns', {i: i for i in vRuns.list_runs()})
AvailableLoa = Enum('AvailableLoa', {'pgm':'pgm', 'cm':'cm'})
AvailableTypeOfViolence = Enum('AvailableTV', {'sb': 'sb', 'ns': 'ns', 'os': 'os'})

priogridQuery = Query(default=None, ge=1, le=259200,
                      title="PrioGRID",
                      description="A valid PrioGRID grid identifier (gid) : between 1 and 259200")
monthQuery = Query(default=None, ge=1, le=999,
                   title="month_id",
                   description="A valid ViEWS month_id, where month_id is a sequence with 1 being January 1980")
dateQuery = Query(default=None, regex=r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$',
                  title="date",
                  description="A valid ISO date, in the format YYYY-MM-DD")
countryQuery = Query(default=None, ge=1, le=999,
                     title="country_id",
                     description="A valid ViEWS numeric country_id. See the ViEWS documentation for details")
latitude = Query(default=None, ge=-90, le=90,
                 title="latitude",
                 description="A valid WGS84 latitude (Y-axis), i.e. from -90 to +90, "
                             "where negative numbers indicate the Southern Hemisphere. "
                             "Must be supplied as a float, in decimal degrees (e.g. 61.5, not 61 30N")
longitude = Query(default=None, ge=-180, le=180,
                  title="longitude",
                  description="A valid WGS84 latitude (X-axis), i.e. from -180 to +180, "
                              "where negative numbers indicate the Western Hemisphere. "
                              "Must be supplied as a float, in decimal degrees (e.g. 61.5, not 61 30E")
isDataQuery = Query(default=True, title="Return Model Tree metadata + Model data or just metadata",
                    description="True (the default) will return both the Model Tree Metadata for the given path "
                                "as well as the data itself. False will only retrieve the Model Tree Metadata")
isStepsQuery = Query(default=False, title="Include stepwise Predictions",
                     description="[WARNING]: Only for advanced use. \n"
                                 "If True, will also yield all individual steps for the n-step ahead models. "
                                 "Defaults to False. Only use if you fully understand the ViEWS methodology "
                                 "and need the individual steps. Due to large datasizes, reduce the pagesize for"
                                 "best results. "
                                 "Note that this flag only makes sense if data = True and has no effect for"
                                 "dinamically simulated (dynasim/ds) models or similar.")

def __subset_helper(cur_run, loa=None, tv=None, model = None):
    if loa is None:
        return cur_run
    if loa == 'pgm':
        subset = cur_run.model_tree.pgm
    else:
        subset = cur_run.model_tree.cm

    if tv is None:
        return subset
    if tv == 'sb':
        subset = subset.sb
    if tv == 'ns':
        subset = subset.ns
    if tv == 'os':
        subset = subset.os

    if model is not None:
        subset = subset

    return subset

def __next_urls(request: Request, page_count:int):
    """
    Take a raw Starlette URL (FastAPI URL handler) and manipulate it to produce the next and previous page
    If page outside of the domain of the page count, return an empty string instead.
    Pages are 1-indexed, i.e. first page is 1. If no paging, or page < 1, assumes page 1.

    :param request: a Starlette raw request
    :param page_count: The total number of paging
    :return: (next_url, prev_url): as urls.
    """

    raw_query_params = request.query_params.__dict__['_dict']
    print("RQP:", raw_query_params)

    try:
        cur_page = int(request.query_params['page'])
    except:
        cur_page = 1

    if cur_page < 1:
        cur_page = 1

    if cur_page > 1:
        raw_query_params_prev = deepcopy(raw_query_params)
        raw_query_params_prev['page']=cur_page-1
        prev_url = request.url.replace_query_params(**raw_query_params_prev)._url
    else:
        prev_url = ''

    if cur_page < page_count:
        raw_query_params_next = deepcopy(raw_query_params)
        raw_query_params_next['page']=cur_page+1
        next_url = request.url.replace_query_params(**raw_query_params_next)._url
    else:
        next_url = ''
    return next_url, prev_url

@app.get("/")
async def get_root():
    """
    :return: Just the run ids
    """
    return {'runs': vRuns.list_runs()}

@app.get("/{run}")
async def get_run(run: AvailableRuns):
    """
    :param run: One of the available rus
    :return: the model without data; it's impossible to supply data across LOAs that makes sense to parse.
    """
    cur_run = vRuns.get_run(run.value)
    cur_run.fetch_model_tree()

    simple_subset = simpleFactory(cur_run.model_tree)

    return {'model_tree': cur_run.model_tree,
            'models': simple_subset.simple,
            'data': None,
            'msg': 'To get data, select at least a LOA'}

@app.get("/{run}/{loa}")
async def get_run(run: AvailableRuns, loa: AvailableLoa, request: Request,
                  pagesize: int = Paging.pagesize,
                  page: int = Paging.page,
                  steps: bool = isStepsQuery,
                  data: bool = isDataQuery,
                  priogrid: List[int] = priogridQuery,
                  countryid: List[int] = countryQuery,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  lat_north_east: float = latitude,
                  lon_north_east: float = longitude,
                  lat_south_east: float = latitude,
                  lon_south_west: float = longitude):

    cur_run = vRuns.get_run(run.value)
    cur_run.fetch_model_tree()
    subset = __subset_helper(cur_run, loa=loa.value)

    simple_subset = simpleFactory(subset)

    if data:
        data_fetcher = DBModel.PageFetcher(run=cur_run,
                                       loa=loa.value,
                                       model_list=simple_subset.simple,
                                       page_size=pagesize,
                                       components=steps)

        data_fetcher.register_where_priogrid(priogrid)
        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_countryid(countryid)

        row_count, page_count = data_fetcher.total_counts()
        next_url, prev_url  = __next_urls(request, page_count=page_count)
        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': subset,
                'models': simple_subset.simple,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': data_fetcher.fetch(page=page)}
    else:
        return {'next_page': '',
                'prev_page': '',
                'model_tree': subset,
                'models': simple_subset.simple}

@app.get("/{run}/{loa}/{tv}")
async def get_run(run: AvailableRuns, loa: AvailableLoa, tv: AvailableTypeOfViolence, request: Request,
                  pagesize: int = Paging.pagesize,
                  page: int = Paging.page,
                  steps: bool = isStepsQuery,
                  data: bool = isDataQuery,
                  priogrid: List[int] = priogridQuery,
                  countryid: List[int] = countryQuery,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  lat_north_east: float = latitude,
                  lon_north_east: float = longitude,
                  lat_south_east: float = latitude,
                  lon_south_west: float = longitude):


    cur_run = vRuns.get_run(run.value)
    cur_run.fetch_model_tree()

    subset = __subset_helper(cur_run, loa=loa.value, tv=tv.value)
    simple_subset = simpleFactory(subset)


    if data:
        data_fetcher = DBModel.PageFetcher(run=cur_run,
                                       loa=loa.value,
                                       model_list=simple_subset,
                                       page_size=pagesize,
                                       components=steps)

        data_fetcher.register_where_priogrid(priogrid)
        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_countryid(countryid)

        row_count, page_count = data_fetcher.total_counts()
        next_url, prev_url  = __next_urls(request, page_count=page_count)
        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': subset,
                'models': simple_subset,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': data_fetcher.fetch(page=page)}
    else:
        return {'next_page': '',
                'prev_page': '',
                'model_tree': subset,
                'models': simple_subset}


@app.get("/{run}/{loa}/{tv}/{model}")
async def get_run(run: AvailableRuns, loa: AvailableLoa, tv: AvailableTypeOfViolence, model: AllModels, request: Request,
                  pagesize: int = Paging.pagesize,
                  page: int = Paging.page,
                  steps: bool = isDataQuery,
                  data: bool = isStepsQuery,
                  priogrid: List[int] = priogridQuery,
                  countryid: List[int] = countryQuery,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  lat_north_east: float = latitude,
                  lon_north_east: float = longitude,
                  lat_south_east: float = latitude,
                  lon_south_west: float = longitude):

    cur_run = vRuns.get_run(run.value)
    cur_run.fetch_model_tree()

    subset = __subset_helper(cur_run, loa=loa.value, tv=tv.value)
    simple_subset = simpleFactory(subset)

    if model.value not in simple_subset:
        return {'msg': f'Error. {model.value} is not an available model in the run'}

    model_tree = [i for i in subset if model.value == i['parent']] + [i for i in subset if model.value == i['node']]
    model_list = [] + [model.value]

    if data:
        data_fetcher = DBModel.PageFetcher(run=cur_run,
                                       loa=loa.value,
                                       model_list=model_list,
                                       page_size=pagesize,
                                       components=steps)

        data_fetcher.register_where_priogrid(priogrid)
        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_countryid(countryid)

        row_count, page_count = data_fetcher.total_counts()
        next_url, prev_url  = __next_urls(request, page_count=page_count)
        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': model_tree,
                'models': model_list,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': data_fetcher.fetch(page=page)}
    else:
        return {'next_page': '',
                'prev_page': '',
                'model_tree': model_tree,
                'models': model_list}


