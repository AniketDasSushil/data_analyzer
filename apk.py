import pandas as pd
import streamlit as st
from plotly import express as px
st.title('Data Analyzer')
st.caption('~made by aniket das')
file = st.file_uploader('upload your csv file here')
if file:
    x = pd.read_csv(file)
    base_column = st.selectbox(label='select the base column',options=x.columns)
    analysis_column = st.selectbox(label='select the analysis column',options=x.columns,)
    analysis = x.groupby(base_column)[analysis_column].value_counts(normalize=True).to_frame()
    analysis = analysis.unstack().reset_index()
    analysis = analysis.set_index(base_column)
    analysis = analysis.T*100
    col = analysis.columns
    analysis[col] = analysis[col].applymap('{:,.2f}%'.format)
    st.dataframe(analysis)
    st.header(analysis_column)
    fig = px.bar(x=x[analysis_column],color=x[base_column],barmode='group',template='presentation')
    fig.update_layout(autosize=False,width=800,height=400)
    st.plotly_chart(fig)
    
    data = analysis.to_csv().encode('utf-8')
    
    st.download_button('download',data,'file.csv','text/csv',key='download-csv')
