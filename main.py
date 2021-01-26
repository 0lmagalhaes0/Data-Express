import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import altair as alt
import base64
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<h1 style='text-align: center; color: darkred;'>DATA ANALYSIS EXPRESS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Let's clean, organize, format and create visualizations for your raw data</h1>", unsafe_allow_html=True)

# LOAD
st.write(" --- ")
st.subheader("Load your Dataset")

path = st.file_uploader("Choose a file", type=['csv'])
if path is None:
    st.warning("Please load your dataset in CSV format")
    st.stop()
else:
    data = pd.read_csv(path)
    col = data.columns.values
    st.write("This dataset has a total of",len(data),"rows and",len(data.columns),"columns.")
    st.write("This is a small piece of it:")
    st.write(data.head(3))


# DELETE COLUMNS
def delete_columns():
    global data
    global col
    del_cols = st.multiselect("Choose the columns you wish to delete:",(col))
    for i in del_cols:
        data.drop([i], axis=1, inplace=True)

    st.write("Your dataset now has a total of ", len(data), " rows and ", len(data.columns), " columns.")
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)

    options = ["No","Yes"]
    change_count = 1
    old_count = 1
    new_count = 1
    while True:
        change_names = st.selectbox("Would you like to rename a column?",options,key=change_count)
        if change_names == "Yes":
            tb_renamed = st.selectbox("Select the column to be renamed:",col,key=old_count)
            new_name = st.text_input("Write the new name:",key=new_count)
            data = data.rename(columns={str(tb_renamed):str(new_name)})
            change_count += 1
            old_count += 1
            new_count += 1
            continue
        if change_names == "No":
            break
    st.write(data.head(3))
    return""

st.write(" --- ")
st.header("DATA CLEANING")
if st.checkbox("Select me to delete or rename columns"):
    st.subheader("Delete and Rename Columns")
    delete_columns()


# REVISION
def revision():
    global data
    st.write(data)
    st.write("If you want to manually fix any specific cell's content, use the fields below:\n"
             "(CAREFUL - it will change ALL fields that match your text, in all columns)")
    wrong = st.text_input("copy here the wrong value")
    right = st.text_input("write here the correct value")
    data = data.replace(str(wrong),str(right))
    st.write(data)
    return ""

st.write(" --- ")
if st.checkbox("Select me to manually review your entire data and change any values"):
    st.subheader("Data Revision")
    revision()


# FORMATTING
def boolify():
    global data
    global col
    bool_type = st.multiselect("Choose the columns you want to convert to Boolean (True/False):", (col))
    for i in bool_type:
        data[i] = data[i].astype(bool)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

def integerify():
    global data
    global col
    int_type = st.multiselect("Choose the columns you want to convert to Integer (Full Numbers):", (col))
    for j in int_type:
        data[j] = data[j].astype(int)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

def floatify():
    global data
    global col
    float_type = st.multiselect("Choose the columns you want to convert to Float (Numbers with Decimals):", (col))
    for n in float_type:
        data[n] = data[n].astype(float)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

def stringify():
    global data
    global col
    str_type = st.multiselect("Choose the columns you want to convert to Object (Text):", (col))
    for l in str_type:
        data[l] = data[l].astype(str)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

def dateify():
    global data
    global col
    change_count = 1
    old_count = 1
    new_count = 1
    while True:
        timely2 = ["%Y-%m-%d %H:%M:%S","%Y-%m-%d","%Y,%m","%m-%d","%Y","%m","%d","%H:%M:%S","%H:%M","%H"]
        timely = ["date & hour", "date"]
        tb_renamed = st.selectbox("Select the column to be reformatted:", col, key=old_count)
        st.write("Legend: Years=%Y, months=%m, days=%d, hours=%H, minutes=%M, seconds=%S")
        new_name = st.selectbox("Choose the date/time format that best fit your column:",timely,key=new_count)
        if new_name == "date & hour":
            data[tb_renamed] = pd.to_datetime(data[tb_renamed],errors="ignore")
        elif new_name == "date":
            data[tb_renamed] = pd.to_datetime(data[tb_renamed], errors="ignore")
            data[tb_renamed] = data[tb_renamed].dt.date

        change_count += 1
        old_count += 1
        new_count += 1
        change_names = st.selectbox("Do you have any other column to convert to Date/Time?", options=("No","Yes"),key=change_count)
        if change_names == "Yes":
            continue
        elif change_names == "No":
            break

    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

st.write(" --- ")
if st.checkbox("Select me to change the format of your data (useful for dates, numbers, coordinates, etc) (for better chart "
               "compatibility, please convert dates to \"data & hour\" and booleans to text)"):
    st.subheader("Formatting your Data")
    formats = ["Select","Integer (Full Numbers)","Float (Numbers with Decimals)","String (Text)","Boolean (True/False","Date & Time"]
    format_choice = st.multiselect("Choose the formats to which you want to change your wrong columns:",formats)
    for i in format_choice:
        if i == formats[1]:
            integerify()
        elif i == formats[2]:
            floatify()
        elif i == formats[3]:
            stringify()
        elif i == formats[4]:
            boolify()
        elif i == formats[5]:
            dateify()


# NAN
def nananan():
    global data
    global col
    fill_text = ""
    nan_method_list = ["Select",
                       "Delete rows with invalid/empty fields",
                       "Fill empty fields with mean value (numbers)",
                       "Fill empty fields with specific value (text)"]
    fill_choice = st.selectbox("Now we should handle the empty/invalid fields (NaN). Choose below your preferred "
                               "method:",nan_method_list)
    if fill_choice == nan_method_list[1]:
        data= data.dropna(axis=0)
    if fill_choice == nan_method_list[2]:
        data = data.fillna(data.mean())
    if fill_choice == nan_method_list[3]:
        fill_text = st.text_input("Type here the value to fill ALL empty fields (as TEXT type)")
        data = data.fillna(fill_text)

    st.write("Your dataset now has a total of ", len(data), " rows and ", len(data.columns), " columns.")
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    st.write(info)
    return ""

st.write(" --- ")
if st.checkbox("Select me to handle empty and invalid data"):
    st.subheader("Empty and Invalid Fields (NaN)")
    nananan()


# SAVE FILE
st.subheader("Save Your Clean File")

def get_table_download_link(data):
    file_name = st.text_input("Choose your file's name:")
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return f'<a href="data:file/csv;base64,{b64}" download="'+file_name+'.csv">Download csv file</a>'

st.markdown(get_table_download_link(data), unsafe_allow_html=True)



# CHARTS
def geograph():
    global data
    global col

    latitude = st.selectbox("Select Latitude Column:", col, key=latitudecount)
    longitude = st.selectbox("Select Longitude Column:", col,key=longitudecount)
    filtering = st.checkbox("Filter your displayed results", key=filteringcount)
    if filtering == True:
        map_filter = st.selectbox("Choose the column:",col,key=map_filtercount)
        filterS = ["select"]
        for i in data[map_filter].unique():
            filterS.append(i)
        filter = st.radio("Choose your filter:",filterS,key=filtercount)
        st.warning("If your filter is boolean (True/False), you must first convert the column to string (Text).")
        for i in filter:
            data = data.loc[data[map_filter] == filter]
    data.rename(columns={latitude:"latitude",longitude:"longitude"},inplace=True)
    st.map(data)
    return ""


def bars():
    global data
    global col

    col = data.columns.values
    bar_col = st.selectbox("Choose the column(s) to exhibit:",col,key=bar_colcount)
    filtering = st.checkbox("Filter your displayed results",key=filteringcount)
    if filtering == True:
        map_filter = st.selectbox("Choose the column:", col, key=map_filtercount)
        filterS = ["select"]
        for i in data[map_filter].unique():
            filterS.append(i)
        filter = st.radio("Choose your filter:", filterS, key=filtercount)
        st.warning("If your filter is boolean (True/False), you must first convert the column to string (Text).")
        for i in filter:
            data = data.loc[data[map_filter] == filter]
    st.bar_chart(data[bar_col].value_counts())
    return ""


def distribution():
    global data
    global col

    x_col = st.selectbox("Choose column for X axis:", col, key=x_colcount)
    y_col = st.selectbox("Choose column for Y axis:", col, key=y_colcount)
    filtering = st.checkbox("Filter your displayed results", key=filteringcount)
    if filtering == True:
        map_filter = st.selectbox("Choose the column:",col,key=map_filtercount)
        filterS = ["select"]
        for i in data[map_filter].unique():
            filterS.append(i)
        filter = st.radio("Choose your filter:",filterS,key=filtercount)
        st.warning("If your filter is boolean (True/False) or numeric, please first convert the column to string (Text).")
        for i in filter:
            data = data.loc[data[map_filter] == filter]

    fig2 = plt.scatter(x=data[x_col], y=data[y_col])
    fig2 = plt.show()
    st.pyplot(fig2)
    return ""


def pie():
    global data
    global col

    all_columns = data.columns.to_list()
    column_to_plot = st.selectbox("Select 1 Column", all_columns,key=map_filtercount)
    filter = st.checkbox("Would you like to group the smaller values?",key=filteringcount)
    if filter == True:
        df = data[column_to_plot].value_counts().sort_values(ascending=False).reset_index()
        df2 = df[:7].copy()
        new_row = pd.DataFrame(data={'index': ['others'],column_to_plot: [df[column_to_plot][7:].sum()]})
        df2 = pd.concat([df2, new_row])
        pie_plot = df2.plot.pie(y=column_to_plot,autopct="%1.1f%%",labels=df2['index'],legend=False)
        st.write(pie_plot)
        st.pyplot()
    else:
        pie_plot = data[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
        st.write(pie_plot)
        st.pyplot()
    return ""


def ml():
    st.write("Thanks for using this app until here. This part is still in development, though, please try again in some days.")
    return ""

st.write(" --- ")
st.header("DATA VISUALIZATION")
st.write("Let's now create some charts to better understand your data.\nATTENTION:"
         " Please keep in mind that any filter created will reflect in subsequent charts.")
chart_types = ["Select", "Bars", "Scatter", "Map", "Pie"]

N = 1
while True:
    latitudecount = N * 0.000001
    longitudecount = N * 0.00001
    filteringcount = N * 0.0001
    map_filtercount = N * 0.001
    filtercount = N * 0.01
    bar_colcount = N * 0.1
    x_colcount = N
    y_colcount = N * 10
    datescount = N * 100
    countcount = N * 1000
    chartcount = N * 10000
    groupcount = N * 100000
    z_colcount = N * 1000000
    chart = st.selectbox("Choose your chart type:", chart_types,key=chartcount)
    if chart == "Map":
        geograph()
        N += 1
        continue
    elif chart == "Bars":
        bars()
        N += 1
        continue
    elif chart == "Scatter":
        distribution()
        N += 1
        continue
    elif chart == "Pie":
        pie()
        N += 1
        continue
    elif chart == "Select":
        if st.checkbox("If you are done with charts, check me to proceed to Machine Learning"):
            ml()
        break
