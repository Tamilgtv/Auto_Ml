#packages

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
from pydataset import data 
dat = data()
from sklearn.preprocessing import MinMaxScaler

st.set_option('deprecation.showPyplotGlobalUse',False)
st.set_page_config(page_title="TDA", page_icon=None, layout='centered', initial_sidebar_state='auto')     


# main function
def main():
    
    #html_css for title
    
    
    ht_tit = """ <div style=background-color:#3366cc;><center><h1 
    style= color:white; font-size: 50px; font-family: "Times New Roman", 
    Times, serif;>TDA ML Explorer </h1></center></div>"""
    st.markdown(ht_tit,unsafe_allow_html=True)
    #TDA project title
       
    #html_css    
    ht_tem = """ <div style=background-color:#3366cc;><center><p 
    style= color:white; font-size: 50px; font-family: "Times New Roman", Times, serif;>Lite Weight Tool To Explore ML </p></center></div>"""
    st.markdown(ht_tem,unsafe_allow_html=True)
    
    #category and data select # Read Data
    
    cat = st.radio('select',['TDA Datasets','Upload your data'])
    df = 0
    filename = 0
    if cat == 'TDA Datasets':
        sel = st.selectbox('select dataset',dat.dataset_id)
        df = data(sel)
    else:
         #file selector

        def file_uploader():
            file = st.file_uploader("select your csv file ")
            return file
        filename = file_uploader()
        
        #intimating status 
        if bool(filename)==False:
            st.info("kindly upload your data for EDA")
        else:
            st.success("File Uploaded Successfully Now you can Proceed to EDA")
        
        
        df = pd.read_csv(filename)

    rows = df.shape[0]
    #select data set by record counts
    if st.checkbox("Show Dataset"):
        number = st.number_input("Number of Records to View",5,rows)
        st.dataframe(df.head(number))
        
    #full dataset  
    if st.checkbox("Show Full dataset"):
        st.dataframe(df)

	# Show Columns
    if st.checkbox("Column Names"):
        st.write(df.columns)
    
    #shape of dataframe
    if st.checkbox('Shape of dataset'):
        'number of rows : ', df.shape[0]
        '\n number of columns : ', df.shape[1]
        
        #Datatypes
    if st.checkbox("Data Types"):
        st.write(df.dtypes)
        
        #variable separation
    if st.checkbox("Select Columns To View "):
        selected_columns = st.multiselect("Select",df.columns)
        new_df = df[selected_columns]
        st.dataframe(new_df)
        
        #check missing values
    if st.checkbox("To check missing values"):
        st.write(df.isna().sum())
        st.write("Total missing values : ",df.isna().sum().sum())
 
        #value_counts
    if st.checkbox("Value Counts"):
        select_col = st.selectbox('select',df.columns)
        st.write("Value Counts by variable",select_col)
        st.write(df[select_col].value_counts())
        
        #Group by counts
    if st.checkbox("Grouby counts"):
        all_columns = df.columns
        primary_col = st.selectbox("Columm to GroupBy",all_columns)
        selected_columns = st.multiselect("Select Columns",all_columns)
        grp = df.groupby(primary_col)[selected_columns].count()
        st.write(grp)

        #Describe data
    if st.checkbox("Describe"):
        st.write(df.describe().T)
        
        #numerical and categorical
    if st.checkbox('view numeric and categorical data'):
        sel=st.radio('select',['numerical','categorical'])
        
        if sel == 'numerical':
            dt = df.select_dtypes(include=['int64','int32','float64','float32'])
            st.text('numerical data')
            st.write(dt) 
        else:
            dt = df.select_dtypes(include='object')
            st.text('categorical data')
            st.write(dt) 

        
        #correlation
    if st.checkbox('Correlation'):
        st.write(df.corr())
        
        #outlier
    if st.checkbox('Outlier'):
        rd = st.radio("select",['outlier data','view boxplot'])
        if rd == 'view boxplot':
            sc = MinMaxScaler().fit_transform(df)
            st.write(plt.boxplot(sc))
            st.pyplot()
        else:
            
            sel = st.selectbox('select column',df.columns)     
            location=[]
            i = sel
            #print(i)
            q1=df[i].quantile(0.25) 
            q3=df[i].quantile(0.75) 
            iqr=q3-q1
            innerfence=df[i].quantile(0.25)-1.5*iqr
            outerfence=df[i].quantile(0.75)+1.5*iqr
            x3=0;loc = 0
            outlier = []
            for j in df[i]:
                loc = loc+1
                if j>outerfence or j<innerfence:
                    #print(j)
                    x3=x3+1
                    outlier.append(j)
                    #fi[i]=fi.drop(j)
                    location.append(loc-1)
                    #print('total no of outliers : ',x3,'\nnum of non outliers : ',x2)
            if x3==0:
                st.success("There is no outlier")
            else:
                st.error('outliers spotted')
                st.write('outliers :',outlier)
    
    #visualization html_css title design
    
    html_vis = """ <div style=background-color:#3366cc;><center><p 
    style= color:white; font-size: 100px; font-family: "Times New Roman", Times, serif;>
    Visualization</p></center></div>"""
    st.markdown(html_vis,unsafe_allow_html=True)
    
    if st.checkbox("Correlation plot - Heat map"):
        st.success("Plot Successfully Created")
        a=st.write(sns.heatmap(df.corr(),annot=True))
        st.pyplot(a)
        
        # Customizable Plot
    if st.checkbox('All plots'):
        all_columns_names = df.columns.tolist()
        type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
        selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

        if st.button("Generate cust Plot"):
            st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

        	# Plot By Streamlit
            if type_of_plot == 'area':
                cust_data = df[selected_columns_names]
                st.area_chart(cust_data)

            elif type_of_plot == 'bar':
                cust_data = df[selected_columns_names]
                st.bar_chart(cust_data)

            elif type_of_plot == 'line':
                cust_data = df[selected_columns_names]
                st.line_chart(cust_data)

    		# Custom Plot 
            elif type_of_plot:
                cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
                st.write(cust_plot)
                st.pyplot()
        
        # Count Plot
    if st.checkbox("Count plot"):
        
        all_columns = df.columns
        primary_col = st.selectbox("Columm to GroupBy",all_columns)
        selected_columns = st.multiselect("Select Columns",all_columns)
        if st.button("Generate Plot"):
            if selected_columns:
                grp = df.groupby(primary_col)[selected_columns].count()
        else:
            grp = df.iloc[:,-1].value_counts()
        st.write(grp.plot(kind="bar"))
        st.pyplot()
        
        #3366cc
    st.markdown(""" <div style=background-color:#3366cc;><center><p 
    style= color:white; font-size: 100px; font-family: "Times New Roman", Times, serif;>
    ML - Supervised Learning</p></center></div>""",unsafe_allow_html=True)
        
        
        
    st.markdown("""<style>
                body {background-color:#ccccff;}</style> """, unsafe_allow_html=True)

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)  


if __name__ == '__main__':
    main()
    
    


