#!/usr/bin/env python
# coding: utf-8

# I've referred to this blog post [https://stmorse.github.io/journal/espn-fantasy-v3.html] to get the majority of the fantasy football data. 
import requests
import json
from ff_maps import POSITION_MAP, PRO_TEAM_MAP, ACTIVITY_MAP, espn_ff_api_views 

def get_credentials(filename): 
    with open(filename) as ff_cookies:
        cookie_data = json.load(ff_cookies)
    return cookie_data 

def fetch_data(credentials, views, datafolder):
    #Currently excluding prior 2019 
    #TODO: change from JSON to pickle? Currently JSON for export human readability 
    #Data storage to be evaluated 

    if views == 'ALL':
        views = espn_ff_api_views
    else:
        views = views

    ff_year = credentials['ff_year']
    league_id = credentials['league_id']
    swid = credentials['swid']
    espn_s2 = credentials['espn_s2']

    #ESPN URL constructor thanks to this post: https://stmorse.github.io/journal/espn-fantasy-v3.html
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{ff_year}/segments/0/leagues/{league_id}'.format(ff_year = str(ff_year), league_id = str(league_id))

    #TODO: extend upon view selection 
    if not views:
        views = espn_ff_api_views

    for view in views:
        r = requests.get(url,     
                        cookies={"swid": swid,
                                "espn_s2": espn_s2},
                        params={"view": view})

        with open('{}ff_view_{}.json'.format(datafolder,view), 'w+') as out:
            json.dump(r.json(), out)

def prep_data():
    

if __name__ == '__main__':

    run_data = input('Do you wish to recreate ff json data? (Y/N): ')

    #TODO: error handling
    if run_data == 'Y':
        credentials = get_credentials('./ff_cookies/cookies.json')
        #Note: views are currently passed as a list and ./ff_data/ is the default storage folder
        fetch_data(credentials, 'ALL', './ff_data/)  
        
