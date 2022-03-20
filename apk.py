import pandas as pd
import streamlit as st
st.title('Data Analyzer')
st.caption('~made by aniket das')
file = st.file_uploader('upload your csv file here')
if file:
    x = pd.read_csv(file)
    base_column = st.selectbox(label='select the base column',options=x.columns)
    analysis_column = st.selectbox(label='select the analysis column',options=x.columns)
    analysis = x.groupby(base_column)[analysis_column].value_counts(normalize=True).to_frame()
    st.table(analysis)
    data = analysis.to_csv().encode('utf-8')
    st.download_button('download',data,'file.csv','text/csv',key='download-csv')