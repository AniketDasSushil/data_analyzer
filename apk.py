import pandas as pd
import streamlit as st
import numpy as np
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
    if base_column != analysis_column:
        st.write('percent wise analysis')
        analysis = x.groupby(base_column)[analysis_column].value_counts(normalize=True).to_frame()
        dis = analysis.copy()
        analysis = analysis.unstack().reset_index()
        analysis = analysis.set_index(base_column)
        analysis = analysis*100
        col = analysis.columns
        analysis.replace(np.nan,0,inplace=True)
        analysis[col] = analysis[col].applymap('{:,.2f}%'.format)
        st.table(analysis)
        data = analysis.to_csv().encode('utf-8')
    
        st.download_button('download',data,'file.csv','text/csv',key='download-csv')
        st.write('count wise analysis')
        count = x.groupby(base_column)[analysis_column].value_counts().to_frame()
        count = count.unstack().reset_index()
        count = count.set_index(base_column)
        count_col = count.columns
        count.replace(np.nan,0,inplace=True)
        count['total'] = count.sum(axis=1)
        count.loc['Total'] = count.sum()
        st.table(count)
        c_data = count.to_csv().encode('utf-8')
        st.download_button('download',c_data,'file.csv','text/csv',key='download-count-csv')
    if base_column != analysis_column:
        dis.rename(columns={analysis_column:'percent'},inplace=True)
        dis = dis.reset_index()
        dis['percent'] = dis['percent']*100
        fig = px.bar(y=dis['percent'],x=dis[base_column],title=analysis_column,color=dis[analysis_column],template='simple_white',labels={'y':'percent','x':base_column},text=dis['percent'].apply(lambda x: "{0:1.2f}%".format(x)))
       
        st.plotly_chart(fig)
        do = st.selectbox('do a chi-square test ?',options=['yes','no'])
        if do == 'yes':
            for k in range(0,len(count)):
                st.write()
            st.write(count[count.columns[-1]].iloc[-1])
            st.write(count[count.columns[0]].iloc[-1])
            st.write(count.iloc[0].iloc[-1])
            st.write(count)
    
    
    
    
