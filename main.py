import streamlit as st
import my_functions as f
from main_lib import my_finance
import time
import datetime
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import pandas as pd
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('Stock forecast dashboard')

# ---- Side Bar
st.sidebar.header("Please Filter Here: ")
st.sidebar.text("""
^GSPC = S&P 500 
^IXIC = NASDAQ 
DJI = Dow Jones 
XU100 = BIST
""")
# Select Box
window_selection_c = st.sidebar.container()  # create an empty container in the sidebar
window_selection_c.markdown("Index Selection")  # add a title to the sidebar container
index = ("^GSPC", "^IXIC", "^DJI", "XU100")

# Selection of index
index_selection = window_selection_c.selectbox("Select Index  ", index)
stocks = f.get_stocks(index_selection)
selected_stocks = window_selection_c.multiselect("select stock", stocks)
# Date Input
window_selection_c = st.sidebar.container()
window_selection_c.markdown("Time Duration")
# From Time
time_from = st.sidebar.date_input("From time", datetime.date(2022, 1, 1))
time_to = st.sidebar.date_input("To time", datetime.datetime.now())


# Buton Setting
button = st.sidebar.button("Run :)")

# Main


#Download Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def main_dataframe():
    if button == True:
        delta=datetime.timedelta(days=1)
        example = my_finance(time_from, time_to+delta, index_selection, selected_stocks)
        #Return Data
        return_data=example.calculate_return
        st.dataframe(return_data,1000,500)

        #Summary Data
        summary=example.summary_data()
        st.dataframe(summary["Total Returns"])
        st.dataframe(summary.style.format("{:.6}"),1000,1000)
        # Correlation Matrix
        correlation_matrix=example.generalCorrelation()
        st.dataframe(correlation_matrix,1000)
        # Total Return Graph
        st.markdown("Total Returns")
        st.line_chart(summary["Total Returns"])

        # Cooeffienct Graph
        st.markdown("Cooeffienct Graph")
        st.bar_chart(summary["Cooefficent of Variation"])

        #Headmap of Correlation
        st.markdown("Headmap of  Correlation")
        fig, ax = plt.subplots(figsize=(10,10))
        sns.heatmap(correlation_matrix, ax=ax,linewidths=.5)
        st.pyplot(fig)

        # # Summary Graph
        # df = pd.concat([summary["mean"], summary["Beta"]],axis=1)
        # st.line_chart(df)


        # Download
        df_xlsx = to_excel(return_data)
        st.download_button(label='📥 Download Return Data',
                           data=df_xlsx,
                           file_name='df_test.xlsx')
main_dataframe()
