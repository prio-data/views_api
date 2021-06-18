from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import StreamingResponse

from starlette.requests import Request
from enum import Enum
from typing import Optional, List
from libdb import DBModel
from libdb.ViEWSModel import ModelTV, ModelLOA, simpleFactory
from libdb.APIConfig import Paging
from copy import deepcopy
import uvicorn
import io
import csv

def makecsv(datastream, page=1, total_pages=0):
    stream = io.StringIO()
    w = csv.writer(stream)

    try:
        length = len(datastream)
    except:
        length = 0
    if length == 0:
        w.writerow([])
    else:
        w.writerow(datastream[0].keys())
        w.writerows(datastream)

    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=forecasts_p{page}.csv"
    response.headers["X-Total-Pages"] = f"{total_pages}"
    return response

app = FastAPI()
vRuns = DBModel.Runs()

AllModels = Enum('AllModels', {i: i for i in vRuns.dirty_full_model_list()})
AvailableRuns = Enum('AvailableRuns', {i: i for i in vRuns.list_runs()})
AvailableLoa = Enum('AvailableLoa', {'pgm':'pgm', 'cm':'cm'})
AvailableTypeOfViolence = Enum('AvailableTV', {'sb': 'sb', 'ns': 'ns', 'os': 'os', 'px': 'px'})

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
isCsv = Query(default=False, title="Return CSV instead of JSON.",
                description="If True, return a CSV file. The file is called forecast_p{$PAGE_NUMBER}. "
                            "No metadata is returned, except the total number of pages."
                            "This is returned as the X-Total-Pages HTTP header")
isEscwa = Query(default=False, title="Return only ESCWA countries.",
                description="If True, clears all other geographic filters and returns data for ESCWA countries")
isStepsQuery = Query(default=False, title="Include stepwise Predictions",
                     description="[WARNING]: Only for advanced use. \n"
                                 "If True, will also yield all individual steps for the n-step ahead models. "
                                 "Defaults to False. Only use if you fully understand the ViEWS methodology "
                                 "and need the individual steps. Due to large datasizes, reduce the pagesize for"
                                 "best results. "
                                 "Note that this flag only makes sense if data = True and has no effect for"
                                 "dinamically simulated (dynasim/ds) models or similar.")
isoQuery = Query(default=None, title="ISO 3-letter country code",
                 description="A 3 letter country code for filtering (e.g. JPN for Japan).")


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
    if tv == 'px':
        subset = subset.px

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

    from urllib.parse import urlencode

    # replace_query_params won't work, because FastAPI takes duplicate keys, but python dicts don't.
    # So we need to work with ugly, nasty, string manipulations.

    qpath = request.query_params.__dict__['_list']
    try:
        cur_page = int(request.query_params['page'])
    except:
        cur_page = 1

    max_page = page_count
    next_page = None
    prev_page = None

    if qpath is None:
        qpath = []

    qpath = [i for i in qpath if i[0] != 'page']

    cur_page = 1 if cur_page < 1 else cur_page
    cur_page = max_page if cur_page > max_page else cur_page

    if cur_page == 1:
        next_page = 2 if max_page > 1 else None

    if cur_page > 1 and cur_page < max_page:
        next_page = cur_page + 1
        prev_page = cur_page - 1

    if cur_page == max_page:
        prev_page = cur_page - 1 if cur_page > 1 else None

    qpath_next = deepcopy(qpath) + [('page', next_page)]
    qpath_prev = deepcopy(qpath) + [('page', prev_page)]

    qpath_next = urlencode([(i[0], i[1]) for i in qpath_next if i != ('page', None)])
    qpath_prev = urlencode([(i[0], i[1]) for i in qpath_prev if i != ('page', None)])

    print('prev:', qpath_prev)
    print('next:', qpath_next)

    if next_page is not None:
        next_url = deepcopy(request.url)
        next_url = str(next_url.replace(query=qpath_next))
    else:
        next_url = ''

    if prev_page is not None:
        prev_url = deepcopy(request.url)
        prev_url = str(prev_url.replace(query=qpath_prev))
    else:
        prev_url = ''

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
            'msg': 'To get data, select at least a level of analysis (LOA)'}


@app.get("/{run}/{loa}")
async def get_run(run: AvailableRuns, loa: AvailableLoa, request: Request,
                  pagesize: int = Paging.pagesize,
                  page: int = Paging.page,
                  steps: bool = isStepsQuery,
                  data: bool = isDataQuery,
                  priogrid: List[int] = priogridQuery,
                  countryid: List[int] = countryQuery,
                  iso: List[str] = isoQuery,
                  gwno: List[int] = None,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  pg_ne: int = priogridQuery,
                  pg_sw: int = priogridQuery,
                  lat_ne: float = latitude,
                  lon_ne: float = longitude,
                  lat_sw: float = latitude,
                  lon_sw: float = longitude,
                  lat: float = latitude,
                  lon: float = longitude,
                  is_escwa: bool = isEscwa,
                  is_csv: bool = isCsv):
    #Escwa
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
        data_fetcher.register_where_countryid(countryid)
        data_fetcher.register_where_iso(iso)
        data_fetcher.register_where_gwno(gwno)
        data_fetcher.register_where_coord(lat,lon)
        data_fetcher.register_where_bbox_pg(pg_ne, pg_sw)
        data_fetcher.register_where_bbox_coord(corner1_lat=lat_ne, corner1_lon=lon_ne,
                                               corner2_lat=lat_sw, corner2_lon=lon_sw)
        if is_escwa:
            data_fetcher.register_where_escwa()

        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_dates(date_start, date_end)

        dataset = data_fetcher.fetch(page=page)
        row_count, page_count = data_fetcher.total_counts()

        if is_csv:
            return makecsv(dataset, page, page_count)

        next_url, prev_url  = __next_urls(request, page_count=page_count)
        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': subset,
                'models': simple_subset.simple,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': dataset}
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
                  iso: List[str] = isoQuery,
                  gwno: List[int] = None,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  pg_ne: int = priogridQuery,
                  pg_sw: int = priogridQuery,
                  lat_ne: float = latitude,
                  lon_ne: float = longitude,
                  lat_sw: float = latitude,
                  lon_sw: float = longitude,
                  lat: float = latitude,
                  lon: float = longitude,
                  is_escwa: bool = isEscwa,
                  is_csv: bool = isCsv):


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
        data_fetcher.register_where_countryid(countryid)
        data_fetcher.register_where_iso(iso)
        data_fetcher.register_where_gwno(gwno)
        data_fetcher.register_where_coord(lat,lon)
        data_fetcher.register_where_bbox_pg(pg_ne, pg_sw)
        data_fetcher.register_where_bbox_coord(corner1_lat=lat_ne, corner1_lon=lon_ne,
                                               corner2_lat=lat_sw, corner2_lon=lon_sw)
        if is_escwa:
            data_fetcher.register_where_escwa()

        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_dates(date_start, date_end)

        dataset = data_fetcher.fetch(page=page)
        row_count, page_count = data_fetcher.total_counts()

        if is_csv:
            return makecsv(dataset, page, page_count)

        next_url, prev_url  = __next_urls(request, page_count=page_count)
        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': subset,
                'models': simple_subset,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': dataset}
    else:
        return {'next_page': '',
                'prev_page': '',
                'model_tree': subset,
                'models': simple_subset}


@app.get("/{run}/{loa}/{tv}/{model}")
async def get_run(run: AvailableRuns, loa: AvailableLoa, tv: AvailableTypeOfViolence, model: AllModels, request: Request,
                  pagesize: int = Paging.pagesize,
                  page: int = Paging.page,
                  steps: bool = isStepsQuery,
                  data: bool = isDataQuery,
                  priogrid: List[int] = priogridQuery,
                  countryid: List[int] = countryQuery,
                  iso: List[str] = isoQuery,
                  gwno: List[int] = None,
                  month: List[int] = monthQuery,
                  date_start: str = dateQuery,
                  date_end: str = dateQuery,
                  pg_ne: int = priogridQuery,
                  pg_sw: int = priogridQuery,
                  lat_ne: float = latitude,
                  lon_ne: float = longitude,
                  lat_sw: float = latitude,
                  lon_sw: float = longitude,
                  lat: float = latitude,
                  lon: float = longitude,
                  is_escwa: bool = isEscwa,
                  is_csv: bool = isCsv):

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
        data_fetcher.register_where_countryid(countryid)
        data_fetcher.register_where_iso(iso)
        data_fetcher.register_where_gwno(gwno)
        data_fetcher.register_where_coord(lat,lon)
        data_fetcher.register_where_bbox_pg(pg_ne, pg_sw)
        data_fetcher.register_where_bbox_coord(corner1_lat=lat_ne, corner1_lon=lon_ne,
                                               corner2_lat=lat_sw, corner2_lon=lon_sw)
        if is_escwa:
            data_fetcher.register_where_escwa()

        data_fetcher.register_where_monthid(month)
        data_fetcher.register_where_dates(date_start, date_end)

        row_count, page_count = data_fetcher.total_counts()
        next_url, prev_url  = __next_urls(request, page_count=page_count)
        #exit(1)
        #print(data_fetcher.fetch(page=page))
        dataset = data_fetcher.fetch(page=page)
        if is_csv:
            return makecsv(dataset, page, page_count)

        return {'next_page': next_url,
                'prev_page': prev_url,
                'model_tree': model_tree,
                'models': model_list,
                'row_count': row_count,
                'page_count': page_count,
                'page_cur': page,
                'data': dataset}
    else:
        return {'next_page': '',
                'prev_page': '',
                'model_tree': model_tree,
                'models': model_list}


if __name__ == "__main__":
    # print ("Run this via uvicorn")
    # To debug:
    uvicorn.run(app, host="0.0.0.0", port=8000)


