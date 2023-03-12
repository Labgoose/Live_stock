# Raw Package
import numpy as np
import pandas as pd
import yfinance as yf

#Data viz
import plotly.graph_objs as go

class CCIIndicator(object):
    def __init__(self,
                 low: pd.Series,
                 high: pd.Series,
                 close: pd.Series,
                 n: int = 14,
                 ):
        self._low = low.copy()
        self._high = high.copy()
        self._close = close.copy()
        self._N = n
        self._run()
        pass

    def _run(self):
        self.TP = (self._high + self._low + self._close)/3
        self.MA = self.TP.rolling(window=self._N).mean()
        self.MD = self.TP.rolling(window=self._N).apply(lambda x: abs(x-x.mean()).mean(), raw=False)
        self.cci = (self.TP - self.MA) / (0.015 * self.MD)

    def data(self):
        return pd.Series(self.cci, name='cci')



#Interval required 1 minute
data = yf.download(tickers='PLTR', period='1d', interval='1m')
# print(data)

#declare figure
fig = go.Figure()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], name = 'market data'))

# Add titles
fig.update_layout(
    title='live share price evolution',
    yaxis_title='Stock Price (USD per Shares)')

# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#Show
fig.show()