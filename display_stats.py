import pandas as pd
import os
import json
from pprint import pprint as pp


class Stats:
    def __init__(self) -> None:
        self.results = pd.read_json('results.json') if os.path.isfile('results.json') else None
        
        with open('shots.json', 'r', encoding='utf-8') as f:
            shots = json.load(f)

        self.situations = {
            team: {
                situation: {
                    **{f'{k}_against': v for k, v in stats.pop('against').items()},
                    **stats
                }
                for situation, stats in stats_dict["situation"].items()
            }
            for team, stats_dict in shots.items()
        }


    def __repr__(self) -> str:
        return self.data.to_string()
    

    def __str__(self) -> str:
        return self.data


    def from_corners(self):
        corners = pd.DataFrame.from_dict(
            orient='index',
            data= {
                team: {
                    'mp': self.results[team]['overall']['played'],
                    **situation['FromCorner']
                }
                for team, situation in self.situations.items()
            }
        )
        
        return corners
