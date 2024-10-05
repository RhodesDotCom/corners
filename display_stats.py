import pandas as pd
import os
import json
from pprint import pprint as pp
import plotly.graph_objects as go
import plotly.io as pio


pio.templates.default = 'plotly_white'

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


    # def __repr__(self) -> str:
    #     return self.data.to_string()
    

    # def __str__(self) -> str:
    #     return self.data


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


    def shots(self, situation='corners'):
        method = getattr(self, f'from_{situation}', None)
        if callable(method):
            df = method()
            columns = df.columns
            columns.pop('mp')
            self.plot_graph(df, df.columns)


    def plot_graph(self, df: pd.DataFrame, columns: list):
        fig = go.Figure()

        buttons = []
        visible = True
        for index, column in enumerate(sorted(columns)):
            df.sort_values(by=column, ascending=False, inplace=True)
            fig.add_trace(go.Bar(
                x=df.index,
                y=df[column],
                name=column,
                visible=visible
            ))
            visible = [False]*len(columns)
            visible[index] = True
            buttons.append(
                {
                    'label': column,
                    'method': 'update',
                    'args': [
                        {'visible': visible},
                        {'title': f'{column} per Team'}
                    ]
                }
            )
            visible=False

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': buttons,
                    'direction': 'down',
                    'showactive': True,
                }
            ],
            title=f'{columns[0]} per Team',
            xaxis_title='Teams',
            yaxis_title='Count',
            barmode='group'
        )

        fig.show()


# stats = Stats()
# stats.shots()