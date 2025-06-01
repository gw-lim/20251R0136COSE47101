import plotly.express as px
import pandas as pd 
import os 
import json 

geometry_gj = json.load(open('./eda/서울_자치구_경계_2017.geojson', encoding='utf-8'))
df = pd.read_csv('./data/processed/인프라_통합.csv', encoding='utf-8')

fig = px.choropleth(df, geojson=geometry_gj, locations='자치구명', color='CCTV_밀도',
                                color_continuous_scale='Reds',
                                featureidkey='properties.SIG_KOR_NM')
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(title_text='CCTV 밀도', title_font_size=20)
fig.show()

os.chdir('./')
fig.write_image('CCTV_밀도.png')