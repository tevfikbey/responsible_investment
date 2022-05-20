import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.pyplot as plt
import time


class my_finance():

    def __init__(self,start_date,to_date,index,names):
        self.start_date=start_date
        self.to_date=to_date
        self.index=index
        self.names=names
        self.data=self.get_data()
        self.index_data=self.get_index_data()



    @property
    def calculate_return(self):
        df = pd.DataFrame()
        for i in self.data:
            data_return = self.data[i]["Return"] = self.data[i]["Adj Close"].pct_change(1).dropna()
            df[f"{i} Return"] = data_return
        df[f"{self.index} Return"]=self.index_data["Adj Close"].pct_change(1).dropna()
        return df


    def get_data(self):
        all_data=dict()
        for i in self.names:
            if self.index=="XU100":
                time.sleep(0.3)
                data = yf.download(f"{i}.IS", self.start_date, self.to_date)
                all_data[f"{i}"]=pd.DataFrame(data)
            else:
                time.sleep(0.3)
                data = yf.download(f"{i}", self.start_date, self.to_date)
                all_data[f"{i}"]=pd.DataFrame(data)

        return all_data

    def get_index_data(self):
        if self.index=="XU100":
            data= yf.download(f"{self.index}.IS", self.start_date, self.to_date)
        else:
            data= yf.download(f"{self.index}", self.start_date, self.to_date)
        return data


    # Summary of data
    def summary_data(self):
        sum = self.calculate_return.describe().T
        sum["Beta"]=self.betawithMarket()
        sum["Correlation with Market Index"]=self.correlationwithMarket()
        sum["Cooefficent of Variation"]=self.coefficient_of_variation()
        sum["Total Returns"]=self.totals_of_returns()
        return sum

    #std of data
    def std(self):
        df=self.calculate_return.std()
        return df
    # Means of data
    def means(self):
        df=self.calculate_return.mean()
        return df
    # Cooefficient calculater
    def coefficient_of_variation(self):
        df=self.std()/self.means()
        return df
    # Variance
    def varrianceOfData(self):
        return self.calculate_return.var()

    # Correlations
    def generalCorrelation(self):
        return self.calculate_return.corr()

    def covvariancewithMarket(self):
        return self.calculate_return.cov().iloc[-1]

    #Toplama
    def totals_of_returns(self):
        return self.calculate_return.sum()
    # Beta
    def betawithMarket(self):
        return self.calculate_return.cov().iloc[-1] / self.varrianceOfData().iloc[-1]

    # CorrelationwithMarket
    def correlationwithMarket(self):
        return self.calculate_return.corr().iloc[-1]







        # for i in self.calculate_return.columns:
        #     if i == "XU100 Return":
        #         break
        #     # df=pd.concat([self.calculate_return[f"{i}"],self.calculate_return["XU100 Return"]],axis=1)
        #     # df=pd.DataFrame(df.cov().iloc[0,[1]])
        #
        # return new_df

            # print(df)



if __name__ == "__main__":
    example=my_finance("2022-02-28", "2022-04-16","XU100",["HALKB","YATAS","SASA","AKBNK","ATEKS","YUNSA"])

    print("Return ALL")
    print(example.summary_data())
    print("Return Index")
