import pandas as pd
import os


class CornerStats:
    def __init__(self) -> None:
        self.data = pd.read_json('data.json') if os.path.isfile('data.json') else None
   
    def __repr__(self) -> str:
        return self.data.to_string()
    
    def __str__(self) -> str:
        return self.data
    


data = CornerStats()

print(data.data)