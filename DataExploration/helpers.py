import json
import requests
import pandas as pd
from typing import TypeVar, Union, List

def listify(string_or_list: Union[List, Union[str,int]]) -> List:
    '''Returns [input] for input if not a list'''
    if isinstance(string_or_list, str) or isinstance(string_or_list, int):
        return [string_or_list]
    return string_or_list

def make_url(base,run,loa,tv,model):
    if run is None:
        raise ValueError("You need a Run")
    if loa is None:
        raise ValueError("You need a Level of Analysis")
    ret_path = base.strip('\ /') +'/'+run.strip('\ /')+'/'+loa.strip('\ /')
    if tv == None:
        return ret_path
    ret_path+='/'+tv.strip('\ /')
    if model == None:
        return ret_path
    ret_path +='/'+model.strip('\ /')
    return ret_path

def fetch_df(url):
    cur_url = url[:]
    df = pd.DataFrame()
    while cur_url is not None:
        print('Fetching : ', cur_url)
        cur_url, cur_data, mtree, mlist, page_count = fetch_slice(cur_url)
        df = df.append(cur_data, ignore_index=True)
    return df

def model_url (base,run):
    '''Return just the metadata URL so that you can get what models are available'''
    return f'{base}/{run}?data=False'

#Convert your chosen options in a proper query bit

def make_options(use_sp_filter=False, sp_filter=None,
                 use_t_filter=False, t_filter=None, other=None):
    options = []

    if not use_sp_filter or use_sp_filter is None:
        pass
    elif use_sp_filter in ('iso','gwno','countryid','priogrid'):
        sp_option = listify(sp_filter[use_sp_filter])
        options.append('&'.join([f'{use_sp_filter}={i}' for i in sp_option]))
    elif use_sp_filter == 'latlon':
        options += [ f'''lat={sp_filter['lat']}&lon={sp_filter['lat']}''']
    elif use_sp_filter == 'bbox':
        bbox_str = []
        for key in bbox:
            bbox_str.append(f'{key}={bbox[key]}')
        options.append('&'.join(bbox_str))

    if not use_t_filter or use_t_filter is None:
        pass
    elif use_t_filter in ('month'):
        t_option = listify(t_filter[use_t_filter])
        options.append('&'.join([f'{use_t_filter}={i}' for i in t_option]))
    elif use_t_filter == 'dates':
        options += [f'''date_start={t_filter['date_start']}&date_end={t_filter['date_end']}''']

    try:
        if other['steps']:
            options += ['steps=True']
    except:
        pass

    try:
        if other['page_size'] is not None:
            options += [f'''page_size={other['page_size']}''']
    except:
        pass

    try:
        if not other['data']:
            options += ['data=False']
    except:
        pass

    try:
        if other['custom'] is not None:
            options += [custom]
    except:
        pass

    query_options_string = '?'+'&'.join(options) if len(options)>0 else ''
    return query_options_string

def fetch_runs(base):
    '''Fetches available runs from the API'''
    r = requests.get(base)
    output = r.json()
    return output['runs']

def fetch_slice(next_page_url):
    '''Fetches a slice of data,
    Returns a pointer to the next slice, all metadata, and all data if the data flag is true'''
    r = requests.get(next_page_url)
    output = r.json()
    try:
        #if the data=False, these will not be returned
        next_page_url = output['next_page'] if output['next_page'] != '' else None
        page_count = output['page_count']
        data = pd.DataFrame(output['data'])
    except:
        next_page_url = None
        page_count = 1
        data = None
    model_tree = pd.DataFrame(output['model_tree'])
    model_list = pd.DataFrame(output['models'])
    return next_page_url, data, model_tree, model_list, page_count
