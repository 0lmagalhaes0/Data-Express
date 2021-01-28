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

port = False
if st.sidebar.checkbox("Português"):
    port = True

# LOAD
st.write(" --- ")
if port == False:
    st.subheader("Load your Dataset")
    path = st.file_uploader("Choose a file", type=['csv'])
    if path is None:
        st.warning("Please load your dataset in CSV format")
        st.stop()
    else:
        data = pd.read_csv(path)
        col = data.columns.values
        st.write("This dataset has a total of",len(data),"rows and",len(data.columns),"columns.\nThis is a small piece of it:")
        st.write(data.head(3))
else:
    st.subheader("Carregue seus dados")
    path = st.file_uploader("Escolha seu arquivo", type=['csv'])
    if path is None:
        st.warning("Apenas arquivos CSV (seu arquivo.csv)")
        st.stop()
    else:
        data = pd.read_csv(path)
        col = data.columns.values
        st.write("Seus dados contém ",len(data)," linhas e ",len(data.columns),"colunas.\nAqui está uma pequena amostra:")
        st.write(data.head(3))


# DELETE COLUMNS
def delete_columns():
    global data
    global col
    if port == False:
        del_cols = st.multiselect("Choose the columns you wish to delete:",(col))
    else:
        del_cols = st.multiselect("Escolha as colunas que você deseja apagar:",(col))
    for i in del_cols:
        data.drop([i], axis=1, inplace=True)

    if port == False:
        st.write("Your dataset now has a total of ", len(data), " rows and ", len(data.columns), " columns.")
    else:
        st.write("Seus dados agora contém ", len(data), " linhas e ", len(data.columns), " colunas.")
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)

    if port == False:
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
                col = data.columns.values
                continue
            if change_names == "No":
                break
    else:
        options = ["Não","Sim"]
        change_count = 1
        old_count = 1
        new_count = 1
        while True:
            change_names = st.selectbox("Você gostaria de renomear alguma coluna?",options,key=change_count)
            if change_names == "Sim":
                tb_renamed = st.selectbox("Selecione a coluna a ser renomeada:",col,key=old_count)
                new_name = st.text_input("Digite o novo nome:",key=new_count)
                data = data.rename(columns={str(tb_renamed):str(new_name)})
                change_count += 1
                old_count += 1
                new_count += 1
                col = data.columns.values
                continue
            if change_names == "Não":
                break

    st.write(data.head(3))
    return""

st.write(" --- ")
if port == False:
    st.header("DATA CLEANING")
    if st.checkbox("Select me to delete or rename columns"):
        st.subheader("Delete and Rename Columns")
        delete_columns()
else:
    st.header("LIMPEZA DOS DADOS")
    if st.checkbox("Me selecione para apagar e/ou renomear colunas"):
        st.subheader("Apagar e Renomear Colunas")
        delete_columns()


# REVISION
def revision():
    global data
    st.write(data)
    if port == False:
        st.write("If you want to manually fix any specific cell's content, use the fields below:\n"
                 "(CAREFUL - it will change ALL fields that match your text, in all columns)")
        wrong = st.text_input("copy here the wrong value")
        right = st.text_input("write here the correct value")
        data = data.replace(str(wrong),str(right))
    else:
        st.write("Se você quiser substituir algum valor específico em seus dados, use os campos abaixo:\n"
                 "(CUIDADO - essa mudança afetará TODAS as células dos seus dados cujo conteúdo seja igual ao seu texto)")
        wrong = st.text_input("copie aqui o valor da sua célula errada")
        right = st.text_input("digite aqui o valor correto")
        data = data.replace(str(wrong),str(right))
    st.write(data)
    return ""

st.write(" --- ")
if port == False:
    if st.checkbox("Select me to manually review your entire data and change any values"):
        st.subheader("Data Revision")
        revision()
else:
    if st.checkbox("Me selecione pra revisar manualmente seus dados e alterar qualquer valor"):
        st.subheader("Revisão de Dados")
        revision()


# FORMATTING
def boolify():
    global data
    global col
    if port == False:
        bool_type = st.multiselect("Choose the columns you want to convert to Boolean (True/False):", (col))
    else:
        bool_type = st.multiselect("Escolha as colunas que você deseja converter para Boolean (True/False):", (col))
    for i in bool_type:
        data[i] = data[i].astype(bool)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)
    return ""

def integerify():
    global data
    global col
    if port == False:
        int_type = st.multiselect("Choose the columns you want to convert to Integer (Full Numbers):", (col))
    else:
        int_type = st.multiselect("Selecione as colunas que você deseja converter para Integer (Números inteiros):", (col))
    for j in int_type:
        data[j] = data[j].astype(int)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)
    return ""

def floatify():
    global data
    global col
    if port == False:
        float_type = st.multiselect("Choose the columns you want to convert to Float (Numbers with Decimals):", (col))
    else:
        float_type = st.multiselect("Selecione as colunas que você deseja covnerter para Float (Números com casas decimais):", (col))
    for n in float_type:
        data[n] = data[n].astype(float)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)
    return ""

def stringify():
    global data
    global col
    if port == False:
        str_type = st.multiselect("Choose the columns you want to convert to Object (Text):", (col))
    else:
        str_type = st.multiselect("Selecione as colunas que você deseja converter para Object (Texto):", (col))
    for l in str_type:
        data[l] = data[l].astype(str)
    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)
    return ""

def dateify():
    global data
    global col
    change_count = 1
    old_count = 1
    new_count = 1
    while True:
        timely = ["date & hour", "date"]
        if port == False:
            tb_renamed = st.selectbox("Select the column to be reformatted:", col, key=old_count)
        else:
            tb_renamed = st.selectbox("Selecione as colunas a serem reformatadas:", col, key=old_count)
        if port == False:
            new_name = st.selectbox("Choose the date/time format that best fit your column (known little bug: the date format rewrites your "
                "data to the best date format, but the column will be converted to Text)",timely,key=new_count)
        else:
            new_name = st.selectbox("Selecione o formato de data que lhe seja mais conveniente: (Pequeno bug: ao escolher o formato Date, "
                "seus dados serão reescritos no melhor formato de data, mas a coluna será convertida para Texto)",timely,key=new_count)
        if new_name == "date & hour":
            data[tb_renamed] = pd.to_datetime(data[tb_renamed],errors="ignore")
        elif new_name == "date":
            data[tb_renamed] = pd.to_datetime(data[tb_renamed], errors="ignore")
            data[tb_renamed] = data[tb_renamed].dt.date

        change_count += 1
        old_count += 1
        new_count += 1
        if port == False:
            change_names = st.selectbox("Do you have any other column to convert to Date/Time?", options=("No","Yes"),key=change_count)
            if change_names == "Yes":
                continue
            elif change_names == "No":
                break
        else:
            change_names = st.selectbox("Você tem mais alguma coluna que deseja converter para Data/Hora?", options=("Não","Sim"),key=change_count)
            if change_names == "Sim":
                continue
            elif change_names == "Não":
                break

    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)
    return ""

st.write(" --- ")
if port == False:
    if st.checkbox("Select me to change the format of your data (useful for dates, numbers, coordinates, etc)"):
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
else:
    if st.checkbox("Me selecione para mudar o formato de seus dados (util para datas, números, coordenadas, etc)"):
        st.subheader("Formatando seus Dados")
        formats = ["Selecione","Integer (Números inteiros)","Float (Números com casas decimais)","String (Texto)","Boolean (True/False)","Date & Time"]
        format_choice = st.multiselect("Escolha os formatos para os quais você deseja converter suas colunas erradas:",formats)
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
    if port == False:
        nan_method_list = ["Select",
                       "Delete rows with invalid/empty fields",
                       "Fill empty fields with mean value (numbers)",
                       "Fill empty fields with specific value (text)"]
        fill_choice = st.selectbox("Now we should handle the empty/invalid fields (NaN). Choose below your preferred "
                               "method:",nan_method_list)
    else:
        nan_method_list = ["Selecione",
                       "Apagar linhas que tenham células vazias/inválidas (recomendado em casos de poucas células vazias)",
                       "Preencher automaticamente células vazias/inválidas com a mediana da coluna (para colunas numéricas)",
                       "Preencher automaticamente células vazias/inválidas com algum texto específico"]
        fill_choice = st.selectbox("Agora vamos lidar com células vazias ou inválidas (NaN). Escolha o melhor método:",nan_method_list)
    if fill_choice == nan_method_list[1]:
        data= data.dropna(axis=0)
    if fill_choice == nan_method_list[2]:
        data = data.fillna(data.mean())
    if fill_choice == nan_method_list[3]:
        if port == False:
            fill_text = st.text_input("Type here the value to fill ALL empty fields (as TEXT type)")
        else:
            fill_text = st.text_input("Digite aqui o valor para preencher TODAS as células vazias (como tipo TEXTO)")
        data = data.fillna(fill_text)

    Types = data.dtypes
    NaN = data.isnull().sum(axis=0)
    sample = data.iloc[[1]].T
    info = pd.concat([sample, Types, NaN], axis=1)
    info.columns = ['Row Sample', 'Types', 'NaN']
    col = data.columns.values
    if port == False:
        st.write("Here are a row sample, the type of data and the amount of empty fields (NaN) in each column:")
    else:
        st.write("Aqui está uma linha de amostra, o formato dos dados de cada coluna e a quantidade de campos em "
            "branco ou inválidos em cada coluna:")
    st.write(info)

    if port == False:
        st.write("Your dataset now has a total of ", len(data), " rows and ", len(data.columns), " columns.")
    else:
        st.write("Seus dados agora contém ", len(data), " linhas e ", len(data.columns), " colunas.")
    return ""

st.write(" --- ")
if port == False:
    if st.checkbox("Select me to handle empty and invalid data (NaN)"):
        st.subheader("Empty and Invalid Fields (NaN)")
        nananan()
else:
    if st.checkbox("Me selecione para lidar com células vazias/inválidas (NaN)"):
        st.subheader("Células Vazias e Inválidas (NaN)")
        nananan()


# SAVE FILE
if port == False:
    st.subheader("Save Your Clean File")
else:
    st.subheader("Salve seus dados limpos")

def download_csv(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="Data Express.csv">Download file</a>'

st.markdown(download_csv(data),unsafe_allow_html=True)


# CHARTS
def geograph():
    global data
    global col

    if port == False:
        latitude = st.selectbox("Select Latitude Column:", col, key=latitudecount)
        longitude = st.selectbox("Select Longitude Column:", col,key=longitudecount)
        filtering = st.checkbox("Filter your displayed results", key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Choose the column:",col,key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["select"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Choose your filter:",filterS,key=filtercount)
            for i in filter:
                data = data.loc[data[map_filter] == filter]
        data.rename(columns={latitude:"latitude",longitude:"longitude"},inplace=True)

    else:
        latitude = st.selectbox("Selecione a coluna da Latitude:", col, key=latitudecount)
        longitude = st.selectbox("Selecione a coluna da Longitude:", col,key=longitudecount)
        filtering = st.checkbox("Filtre os resultados", key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Escolha a coluna:",col,key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["selecione"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Escolha seus filtros:",filterS,key=filtercount)
            for i in filter:
                data = data.loc[data[map_filter] == filter]
        data.rename(columns={latitude:"latitude",longitude:"longitude"},inplace=True)

    st.map(data)
    return ""


def bars():
    global data
    global col

    col = data.columns.values
    if port == False:
        bar_col = st.selectbox("Choose the column(s) to exhibit:",col,key=bar_colcount)
        filtering = st.checkbox("Filter your displayed results",key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Choose the column:", col, key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["select"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Choose your filter:", filterS, key=filtercount)
            for i in filter:
                data = data.loc[data[map_filter] == filter]
    
    else:
        bar_col = st.selectbox("Escolha a coluna para exibir:",col,key=bar_colcount)
        filtering = st.checkbox("Filtre os resultados",key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Escolha a coluna:", col, key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["selecione"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Escolha seus filtros:", filterS, key=filtercount)
            for i in filter:
                data = data.loc[data[map_filter] == filter]

    st.bar_chart(data[bar_col].value_counts())
    return ""


def distribution():
    global data
    global col

    if port == False:
        x_col = st.selectbox("Choose column for X axis:", col, key=x_colcount)
        y_col = st.selectbox("Choose column for Y axis:", col, key=y_colcount)
        filtering = st.checkbox("Filter your displayed results", key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Choose the column:",col,key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["select"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Choose your filter:",filterS,key=filtercount)
            for i in filter:
                data = data.loc[data[map_filter] == filter]

    else:
        x_col = st.selectbox("Escolha a coluna para o eixo X:", col, key=x_colcount)
        y_col = st.selectbox("Escolha a coluna para o eixo Y:", col, key=y_colcount)
        filtering = st.checkbox("Filtre os resultados", key=filteringcount)
        if filtering == True:
            map_filter = st.selectbox("Escolha a coluna:",col,key=map_filtercount)
            data[map_filter] = data[map_filter].astype(str)
            filterS = ["selecione"]
            for i in data[map_filter].unique():
                filterS.append(i)
            filter = st.radio("Escolha seu filtro:",filterS,key=filtercount)
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
    if port == False:
        column_to_plot = st.selectbox("Select a Column", all_columns,key=map_filtercount)
        filter = st.checkbox("Would you like to group the smaller values?",key=filteringcount)
    else:
        column_to_plot = st.selectbox("Selecione uma coluna", all_columns,key=map_filtercount)
        filter = st.checkbox("Gostaria de agrupar os valores menores?",key=filteringcount)
    if filter == True:
        df = data[column_to_plot].value_counts().sort_values(ascending=False).reset_index()
        df2 = df[:7].copy()
        if port == False:
            new_row = pd.DataFrame(data={'index': ['Others'],column_to_plot: [df[column_to_plot][7:].sum()]})
        else:
            new_row = pd.DataFrame(data={'index': ['Outros'],column_to_plot: [df[column_to_plot][7:].sum()]})
        df2 = pd.concat([df2, new_row])
        pie_plot = df2.plot.pie(y=column_to_plot,autopct="%1.1f%%",labels=df2['index'],legend=False)
        st.write(pie_plot)
        st.pyplot()
    else:
        pie_plot = data[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
        st.write(pie_plot)
        st.pyplot()
    return ""

st.write(" --- ")
if port == False:
    st.header("DATA VISUALIZATION")
    st.write("Let's now create some charts to better understand your data.\nATTENTION:"
         " Please keep in mind that any filter created will reflect in subsequent charts.")
    chart_types = ["Select", "Bars", "Scatter", "Map", "Pie"]
else:
    st.header("VISUALIZAÇÃO DOS DADOS")
    st.write("Agora vamos criar alguns gráficos para visualizar melhor seus dados.\nATENÇÃO:"
         " Filtros criados para um gráfico vão refletir também nos gráficos subsequentes.")
    chart_types = ["Selecione", "Barras", "Dispersão", "Mapa", "Pizza"]

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
    if port == False:
        chart = st.selectbox("Choose your chart type:", chart_types,key=chartcount)
        if chart == chart_types[3]:
            geograph()
            N += 1
            continue
        elif chart == chart_types[1]:
            bars()
            N += 1
            continue
        elif chart == chart_types[2]:
            distribution()
            N += 1
            continue
        elif chart == chart_types[4]:
            pie()
            N += 1
            continue
        elif chart == chart_types[0]:
            #if st.checkbox("If you are done with charts, check me to proceed to Machine Learning"):
            #    ml()
            break

    else:
        chart = st.selectbox("Escolha seu tipo de gráfico:", chart_types, key=chartcount)
        if chart == chart_types[3]:
            geograph()
            N += 1
            continue
        elif chart == chart_types[1]:
            bars()
            N += 1
            continue
        elif chart == chart_types[2]:
            distribution()
            N += 1
            continue
        elif chart == chart_types[4]:
            pie()
            N += 1
            continue
        elif chart == chart_types[0]:
            #if st.checkbox("Se você já criou todos os gráficos que deseja, me selecione para prosseguir para Machine Learning"):
            #    ml()
            break
