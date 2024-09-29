import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt, timedelta


def get_stats():
    year = 2024
    url = 'https://understat.com/team/{team}/{year}'
    teams = ['Arsenal',
    'Aston Villa',
    'Bournemouth',
    'Brentford',
    'Brighton',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Ipswich',
    'Leicester',
    'Liverpool',
    'Manchester City',
    'Manchester United',
    'Newcastle United',
    'Nottingham Forest',
    'Southampton',
    'Tottenham',
    'West Ham',
    'Wolverhampton Wanderers'
    ]


    team_stats = dict()
    for team in teams:
        print(url.format(team=team.replace(' ','_'), year=year))
        page = requests.get(url.format(team=team.replace(' ','_'), year=year))
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

        team_stats[team] = from_corner

    request = requests.get('https://www.premierleague.com/tables')
    soup = BeautifulSoup(request.text, 'html.parser')

    table = soup.find('tbody', class_='league-table__tbody')
    rows = soup.find_all('tr', attrs={'data-position': True})

    for index, row in enumerate(rows):
        if index == 20:
            break

        row_name = row.get('data-filtered-table-row-name')
        third_td = row.find_all('td')[2].text

        teams_matching = {'Brighton & Hove Albion':'Brighton',
                'Luton Town':'Luton',
                'Tottenham Hotspur': 'Tottenham',
                'West Ham United':'West Ham'
        }

        if row_name in teams_matching:
            team_name = teams_matching[row_name]
            team_stats[team_name]['matches'] = int(third_td)
        else:
            team_stats[row_name]['matches'] = int(third_td)

    with open('data_time.txt', 'w') as f:
        f.write(str(dt.now()))
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(team_stats, f, ensure_ascii=False, indent=4)


# with open('data_time.txt', 'r') as f:
#     last_time_str = f.read()
# try:
#     last_time = dt.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     if (dt.now() - last_time).total_seconds() > 8.64e10:
#         get_stats()
# except:
#     get_stats()

# with open('data.json', 'r', encoding='utf-8') as f:
#     team_stats = json.load(f)

get_stats()

df = pd.DataFrame.from_dict(team_stats)
df = df.transpose()

### HIGHEST xG ###
# print(df.sort_values(by='xG', ascending=False))
### HIGHEST xGA ###
# print(df.sort_values(by='xGA', ascending=False))

### HIGHEST SHOTS AGAINST ####
print(df.sort_values(by='shots_against', ascending=False))

# print(df.sort_values(by='goals_against', ascending=False))


# print(df.sort_values(by='xG', ascending=False))

# df['xG_diff']

######GRAPHS
# shots_a = df['shots_against']/df['matches']
# shots_a = shots_a.sort_values(ascending=False)
# xGA = df['xGA']/df['matches']
# xGA = xGA.sort_values(ascending=False)

# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 12))
# shots_a.plot(kind='bar', ax=axes[0], color='skyblue')
# axes[0].set_title('shots againts')
# # axes[0].set_xlabel('Team')
# axes[0].set_ylabel('Shots')

# xGA.plot(kind='bar', ax=axes[1], color='lightgreen')
# axes[1].set_title('xGA')
# # axes[1].set_xlabel('Team')
# axes[1].set_ylabel('xGA')

# plt.tight_layout()
# plt.show()
            
