import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

import warnings
warnings.filterwarnings('ignore')
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(
  page_title="ESTATÍSTICAS\nSite The Stats Don't Lie - TSDL",
  page_icon='⚽',
  layout="wide")

st.sidebar.title(
    """
    🇧🇷 ESTATÍSTICAS TSDL 🇧🇷
    """)

liga = st.sidebar.selectbox('Escolha a Liga',(
    'Alemanha',
    'Alemanha 2',
    'Austrália',
    'Argentina',
    'Bélgica',
    'Brasil - Série A',
    'Brasil - Série B',
    'Brasil - Série C',
    'Dinamarca',
    'Escócia',
    'Espanha',
    'Espanha 2',
    'França',
    'França 2',
    'Grécia',
    'Holanda',
    'Inglaterra',
    'Inglaterra 2',
    'Itália',
    'Itália 2',
    'Portugal',
    'Suécia',
    'Suíça',
    'Turquia'
    ))

if liga == 'Alemanha':
    url1 = 'https://www.thestatsdontlie.com/football/europe/germany/bundesliga/'
if liga == 'Alemanha 2':
    url1 = 'https://www.thestatsdontlie.com/football/europe/germany/2-bundesliga/'
if liga == 'Austrália':
    url1 = 'https://www.thestatsdontlie.com/football/rest-of-the-world/australia/a-league/'
if liga == 'Argentina':
    url1 = 'https://www.thestatsdontlie.com/football/n-s-america/argentina/primera-division/'
if liga == 'Bélgica':
    url1 = 'https://www.thestatsdontlie.com/football/europe/belgium/pro-league/'
if liga == 'Brasil - Série A':
    url1 = 'https://www.thestatsdontlie.com/football/n-s-america/brazil/serie-a/'
if liga == 'Brasil - Série B':
    url1 = 'https://www.thestatsdontlie.com/football/n-s-america/brazil/serie-b/'
if liga == 'Brasil - Série C':
    url1 = 'https://www.thestatsdontlie.com/football/n-s-america/brazil/serie-c/'
if liga == 'Dinamarca':
    url1 = 'https://www.thestatsdontlie.com/football/europe/denmark/superliga/'
if liga == 'Escócia':
    url1 = 'https://www.thestatsdontlie.com/football/uk-ireland/scotland/premiership/'
if liga == 'Espanha':
    url1 = 'https://www.thestatsdontlie.com/football/europe/spain/la-liga/'
if liga == 'Espanha 2':
    url1 = 'https://www.thestatsdontlie.com/football/europe/spain/segunda-division/'
if liga == 'França':
    url1 = 'https://www.thestatsdontlie.com/football/europe/france/ligue-1/'
if liga == 'França 2':
    url1 = 'https://www.thestatsdontlie.com/football/europe/france/ligue-2/'
if liga == 'Grécia':
    url1 = 'https://www.thestatsdontlie.com/football/europe/greece/super-league/'
if liga == 'Holanda':
    url1 = 'https://www.thestatsdontlie.com/football/europe/holland/eredivisie/'
if liga == 'Inglaterra':
    url1 = 'https://www.thestatsdontlie.com/football/uk-ireland/england/premier-league/'
if liga == 'Inglaterra 2':
    url1 = 'https://www.thestatsdontlie.com/football/uk-ireland/england/championship/'
if liga == 'Itália':
    url1 = 'https://www.thestatsdontlie.com/football/europe/italy/serie-a/'
if liga == 'Itália 2':
    url1 = 'https://www.thestatsdontlie.com/football/europe/italy/serie-b/'
if liga == 'Portugal':
    url1 = 'https://www.thestatsdontlie.com/football/europe/portugal/primeira-liga/'
if liga == 'Suécia':
    url1 = 'https://www.thestatsdontlie.com/football/europe/sweden/allsvenskan/'
if liga == 'Suíça':
    url1 = 'https://www.thestatsdontlie.com/football/europe/switzerland/super-league/'
if liga == 'Turquia':
    url1 = 'https://www.thestatsdontlie.com/football/europe/turkey/super-lig/'

def scout(url):
    headers = {'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    iframe_src = soup.find_all('iframe')
    s = requests.Session() 

    tabelas=[]
    for ifr in iframe_src: 
        _src_str = "{:}".format(ifr["src"]) 
        if "https" not in _src_str: 
            _url = "https:{:}".format(iframe_src[0]["src"]) 
        else: 
            _url = _src_str
        tabelas.append(_url)
        r = s.get(_url)
    return tabelas

urls = [url1+'corners/',url1+'cards/']

for i,url in enumerate(urls):
    tabelas = scout(url)
    if liga != 'Turquia':
        ll = -1
    else:
        ll = -2
    if i == 0:
        df_temp = pd.read_html(tabelas[9])[0]
        df_corner = df_temp[['Unnamed: 12','Unnamed: 15']]
        df_corner = df_corner.drop(df_corner.index[[0,1,ll]], axis=0)
        df_corner.columns = ['TIME', 'MÉDIA ESCANTEIOS']
        df_corner['MÉDIA ESCANTEIOS'] = df_corner['MÉDIA ESCANTEIOS'].astype('float')
        df_corner.set_index('TIME',inplace=True)
    if i == 1:
        df_AmFav = pd.read_html(tabelas[0])[0]
        df_AmCon = pd.read_html(tabelas[1])[0]
        df_VmFav = pd.read_html(tabelas[2])[0]
        df_VmCon = pd.read_html(tabelas[3])[0]

        # CARTÕES AMARELOS GERAL - A FAVOR
        df_YF = df_AmFav[['Unnamed: 12','Unnamed: 15']]
        df_YF.columns = ['TIME','Med_Ama_Fv']
        df_YF = df_YF.drop(df_YF.index[[0,1,ll]], axis=0)
        df_YF.set_index('TIME',inplace=True)

        # CARTÕES AMARELOS GERAL - CONTRA
        df_YC = df_AmCon[['Unnamed: 12','Unnamed: 15']]
        df_YC.columns = ['TIME','Med_Ama_C']
        df_YC = df_YC.drop(df_YC.index[[0,1,ll]], axis=0)
        df_YC.set_index('TIME',inplace=True)

        # CARTÕES VERMELHOS GERAL - A FAVOR
        df_RF = df_VmFav[['Unnamed: 12','Unnamed: 15']]
        df_RF.columns = ['TIME','Med_Verm_Fv']
        df_RF = df_RF.drop(df_RF.index[[0,1,ll]], axis=0)
        df_RF.set_index('TIME',inplace=True)

        # CARTÕES VERMELHOS GERAL - CONTRA
        df_RC = df_VmCon[['Unnamed: 12','Unnamed: 15']]
        df_RC.columns = ['TIME','Med_Verm_C']
        df_RC = df_RC.drop(df_RC.index[[0,1,ll]], axis=0)
        df_RC.set_index('TIME',inplace=True)

        df_cartoes = pd.concat([df_YF,df_YC,df_RF,df_RC],axis=1)
        
        df_cartoes['Med_Ama_Fv'] = df_cartoes['Med_Ama_Fv'].astype('float')
        df_cartoes['Med_Ama_C'] = df_cartoes['Med_Ama_C'].astype('float')
        df_cartoes['Med_Verm_Fv'] = df_cartoes['Med_Verm_Fv'].astype('float')
        df_cartoes['Med_Verm_C'] = df_cartoes['Med_Verm_C'].astype('float')

        df_cartoes['MÉDIA Cartões Amarelos'] = df_cartoes['Med_Ama_Fv'] + df_cartoes['Med_Ama_C']
        df_cartoes['MÉDIA Cartões Vermelhos'] = df_cartoes['Med_Verm_Fv'] + df_cartoes['Med_Verm_C']

        df_cartoes.drop(df_cartoes.columns[:-2],axis=1,inplace=True)
    
df = pd.concat([df_cartoes,df_corner],axis=1)
df.reset_index(inplace=True)

st.title(liga)
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_default_column(min_column_width=5,editable=False,sortable=False,resizable=False,suppressMovable=True)
builder.configure_column("MÉDIA ESCANTEIOS", header_name="MED ESC",width=100)
builder.configure_column("MÉDIA Cartões Amarelos", header_name="MED CA",width=100)
builder.configure_column("MÉDIA Cartões Vermelhos", header_name="MED CV",width=100)
go = builder.build()
jscode = JsCode("""
                function(params) {
                    if (params.data.TIME != 'Senegal') {
                        return {
                            'color': 'white',
                            'backgroundColor': 'darkblue',
                            'fontWeight': 'Bold'
                        }
                    }
                };
                """)
go['getRowStyle'] = jscode

grid_response = AgGrid(df,gridOptions = go,
fit_columns_on_grid_load=True,
theme="alpine",
allow_unsafe_jscode=True)

