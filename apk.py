import pandas as pd
import streamlit as st
from plotly import express as px
st.title('Data Analyzer')
st.caption('~made by aniket das')
file = st.file_uploader('upload your csv file here')
if file:
    try:
        x = pd.read_csv(file)
    except ValueError:
        st.error('error in file format')
    base_column = st.selectbox(label='select the base column',options=x.columns)
    analysis_column = st.selectbox(label='select the analysis column',options=x.columns,)
    analysis = x.groupby(base_column)[analysis_column].value_counts(normalize=True).to_frame()
    dis = analysis.copy()
    analysis = analysis.unstack().reset_index()
    analysis = analysis.set_index(base_column)
    analysis = analysis.T*100
    col = analysis.columns
    analysis[col] = analysis[col].applymap('{:,.2f}%'.format)
    st.dataframe(analysis)
    data = analysis.to_csv().encode('utf-8')
    st.download_button('download',data,'file.csv','text/csv',key='download-csv')
    if base_column != analysis_column:
        dis.rename(columns={analysis_column:'percent'},inplace=True)
        dis = dis.reset_index()
        dis['percent'] = dis['percent']*100
        fig = px.bar(y=dis['percent'],x=dis[base_column],title=analysis_column,color=dis[analysis_column],template='simple_white',labels={'y':'percent','x':base_column},text=dis['percent'].apply(lambda x: "{0:1.2f}%".format(x)))
       
        st.plotly_chart(fig)
    
    
    
    
