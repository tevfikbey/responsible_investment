import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.pyplot as plt
import json


def get_stocks(index:str)-> list:
    with open ("all_data.json","r",encoding="UTF-8") as json_data:
        data=json.load(json_data)
    if index in ("^GSPC","^IXIC","^DJI","XU100"): 
        return [i for i in data[index]]
    else:
        raise Exception("Aranan index bulunamadı")

if __name__ == "__main__":
    a=get_stocks("XU100")
    print(a)
