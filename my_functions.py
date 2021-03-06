import pandas as pd
import numpy as np
from datetime import datetime
import json


def get_stocks(index:str)-> list:
    with open ("all_data.json","r",encoding="UTF-8") as json_data:
        data=json.load(json_data)
    if index in ("^GSPC","^IXIC","^DJI","XU100"): 
        return [i for i in data[index]]
    else:
        raise Exception("Aranan index bulunamad─▒")

if __name__ == "__main__":
    a=get_stocks("XU100")
    print(a)
