import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go


countries = ['brazil', 'united states']
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()


@st.cache(allow_output_mutation=True)
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df


def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig


# CRIANDO UMA BARRA LATERAL
barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Selecione o país:", countries)
acoes = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Selecione o ativo:", acoes)
from_date = st.sidebar.date_input('De:', start_date)
to_date = st.sidebar.date_input('Para:', end_date)
interval_select = st.sidebar.selectbox("Selecione o interval:", intervals)
carregar_dados = st.sidebar.checkbox('Carregar dados')


grafico_line = st.empty()
grafico_candle = st.empty()

# elementos centrais da página
st.title('Stock Monitor')

st.header('Ações')

st.subheader('Visualização gráfica')


if from_date > to_date:
    st.sidebar.error('Data de ínicio maior do que data final')
else:
    df = consultar_acao(stock_select, country_select, format_date(
        from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)
        if carregar_dados:
            st.subheader('Dados')
            dados = st.dataframe(df)
            stock_select = st.sidebar.selectbox
    except Exception as e:
        st.error(e)
