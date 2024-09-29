import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import sys
import time
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


YEAR = 2024
URL = 'https://understat.com/team/{team}/{year}'

NAME_FIXES = {
    'Brighton & Hove Albion':'Brighton',
    'Ipswich Town': 'Ipswich',
    'Leicester City': 'Leicester',
    'Luton Town':'Luton',
    'Tottenham Hotspur': 'Tottenham',
    'West Ham United':'West Ham'
}


def get_stats():

    teams = get_teams()
    team_stats = dict()

    for team_name, stats in teams.items():
        url = URL.format(team=team_name.replace(' ','_'), year=YEAR)

        print(f'Getting data from: {url}')

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        script_tag = soup.find('script', string=lambda x: 'statisticsData' in x)
        json_data = script_tag.text.split('statisticsData = JSON.parse(')[1].split(');')[0].replace('\'', '')
        decoded_json = json_data.encode().decode('unicode-escape')
        as_json = json.loads(decoded_json)
        from_corner = as_json['situation']['FromCorner']

        against_dict = from_corner.pop('against')

        from_corner['shots_against'] = against_dict.get('shots')
        from_corner['goals_against'] = against_dict.get('goals')
        from_corner['xGA'] = against_dict.get('xG')

        team_stats[team_name] = {**stats, **from_corner}
    

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(team_stats, f, ensure_ascii=False, indent=4)
    

def get_teams():
    season_id = {
        "All Seasons": "-1",
        "2024/25": "719",
        "2023/24": "578",
        "2022/23": "489",
        "2021/22": "418",
        "2020/21": "363",
        "2019/20": "274",
        "2018/19": "210",
        "2017/18": "79",
        "2016/17": "54",
        "2015/16": "42",
        "2014/15": "27",
        "2013/14": "22",
        "2012/13": "21",
        "2011/12": "20",
        "2010/11": "19",
        "2009/10": "18",
        "2008/09": "17",
        "2007/08": "16",
        "2006/07": "15",
        "2005/06": "14",
        "2004/05": "13",
        "2003/04": "12",
        "2002/03": "11",
        "2001/02": "10",
        "2000/01": "9",
        "1999/00": "8",
        "1998/99": "7",
        "1997/98": "6",
        "1996/97": "5",
        "1995/96": "4",
        "1994/95": "3",
        "1993/94": "2",
        "1992/93": "1"
    }

    year = f"{YEAR}/{int(str(YEAR)[2:])+1}"
    url = f"https://footballapi.pulselive.com/football/standings"
    headers = {"origin": "https://www.premierleague.com"}
    params = {"compSeasons": {season_id[year]}}

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
    
    # print(len(data['tables']))
    team_stats = data['tables'][0]['entries']

    teams = {}
    for team in team_stats:
        team_name = team['team']['name']

        teams[team_name] = {}
        teams[team_name]['overall'] = team['overall']
        teams[team_name]['home'] = team['home']
        teams[team_name]['away'] = team['away']

    return dict(sorted(teams.items()))
