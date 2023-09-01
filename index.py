from math import isnan
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='HFS Emote Stats', layout='wide')
st.markdown(
    '''
    <style>
        ul[aria-activedescendant] ul[role="option"]:nth-child(n+3):nth-child(-n+7),
        ul[aria-activedescendant] div:nth-child(n+1):nth-child(-n+5),
        div[data-testid="stDecoration"], iframe, footer {
            display: none !important;
        }
        .main .block-container {
            padding-top: 40px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

def get_rankings(df):
    latest_data = dict(zip(df.index, df.iloc[:, -1]))
    num_items = { k: v for k, v in latest_data.items() if not isnan(v) }
    listed_items = list(num_items.items())
    sorted_items = sorted(listed_items, key=lambda item: item[1], reverse=True)
    return { key: rank + 1 for rank, (key, _) in enumerate(sorted_items) }

def legend_ranking(t):
    t.update(legendrank=rankings[t.name] if t.name in rankings else None)

def create_line_graph(df, title_name):
    global rankings
    rankings = get_rankings(df)
    df_transposed = df.T
    fig = px.line(df_transposed)
    fig.update_layout(
        title=title_name,
        legend_title_text=None,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    fig.update_xaxes(title_text='Year_Month')
    fig.update_yaxes(title_text='Count')
    fig.update_traces(hovertemplate='%{x}<br>%{y}')
    fig.for_each_trace(lambda t: legend_ranking(t))
    st.plotly_chart(fig, use_container_width=True)

emotes = pd.read_csv('data/emotes.csv', index_col=[0])
stickers = pd.read_csv('data/stickers.csv', index_col=[0])

st.header('Hololive Fan Server #emote-use-stats')
create_line_graph(emotes, 'Emotes')
create_line_graph(stickers, 'Stickers')
