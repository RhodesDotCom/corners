import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pprint import pprint as pp

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


def main():
    results = get_results()

    # teams = [NAME_FIXES.get(name, name) for name in results.keys()]
    teams = results.keys()
    shots = get_shots(teams)

    with open('results.json', 'w', encoding='utf-8') as f:
         json.dump(results, f, ensure_ascii=False, indent=4)
    with open('shots.json', 'w', encoding='utf-8') as f:
         json.dump(shots, f, ensure_ascii=False, indent=4)


def get_results():
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
    
    team_stats = data['tables'][0]['entries']

    teams = {}
    for team in team_stats:
        team_name = team['team']['name']

        teams[NAME_FIXES.get(team_name, team_name)] = {
            "overall": team['overall'],
            "home": team["home"],
            "away": team["away"]
        }

    return dict(sorted(teams.items()))


def get_shots(teams: list):
    
    stats = {}
    for team_name in teams:
        url = URL.format(team=team_name.replace(' ','_'), year=YEAR)

        print(f'Getting data from: {url}')

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        script_tag = soup.find('script', string=lambda x: 'statisticsData' in x)
        json_data = script_tag.text.split('statisticsData = JSON.parse(')[1].split(');')[0].replace('\'', '')
        decoded_json = json_data.encode().decode('unicode-escape')
        as_json = json.loads(decoded_json)
        
        stats[team_name] = as_json
    
    return stats


main()