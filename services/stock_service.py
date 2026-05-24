import yfinance as yf
import ta
import plotly.graph_objs as go
import json
import plotly

# TECHNICAL INDICATORS
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands


# =========================
# FETCH STOCK DATA
# =========================
def fetch(stock):

    try:

        df = yf.download(stock, period="6mo", interval="1d")

        if df is None or df.empty:
            print("EMPTY DATA")
            return None

        # RESET INDEX
        df = df.reset_index()

        # FIX DATE COLUMN
        if "Date" not in df.columns:
            if "Datetime" in df.columns:
                df.rename(columns={"Datetime": "Date"}, inplace=True)

        # FIX MULTIINDEX
        df.columns = [
            col[0] if isinstance(col, tuple) else col
            for col in df.columns
        ]

        # KEEP REQUIRED
        df = df[
            ["Date", "Open", "High", "Low", "Close", "Volume"]
        ]

        # TYPE CONVERSION
        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

        for col in numeric_cols:
            df[col] = df[col].astype(float)

        # =========================
        # TECHNICAL INDICATORS
        # =========================

        # SMA
        df["SMA_10"] = SMAIndicator(
            close=df["Close"],
            window=10
        ).sma_indicator()

        # EMA
        df["EMA_10"] = EMAIndicator(
            close=df["Close"],
            window=10
        ).ema_indicator()

        # RSI
        df["RSI"] = RSIIndicator(
            close=df["Close"],
            window=14
        ).rsi()

        # MACD
        macd = MACD(close=df["Close"])

        df["MACD"] = macd.macd()

        # Bollinger Bands
        bb = BollingerBands(
            close=df["Close"],
            window=20
        )

        df["BB_HIGH"] = bb.bollinger_hband()
        df["BB_LOW"] = bb.bollinger_lband()

        # REMOVE NaN
        df.dropna(inplace=True)

        print("FINAL DATA:")
        print(df.tail())

        return df

    except Exception as e:
        print("FETCH ERROR:", e)
        return None


# =========================
# CHART
# =========================
def chart(df, stock):

    try:

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=list(df["Date"]),
            open=list(df["Open"]),
            high=list(df["High"]),
            low=list(df["Low"]),
            close=list(df["Close"]),
            name="Candlestick"
        ))

        # SMA LINE
        fig.add_trace(go.Scatter(
            x=list(df["Date"]),
            y=list(df["SMA_10"]),
            mode="lines",
            name="SMA 10"
        ))

        # EMA LINE
        fig.add_trace(go.Scatter(
            x=list(df["Date"]),
            y=list(df["EMA_10"]),
            mode="lines",
            name="EMA 10"
        ))

        fig.update_layout(
            title=f"{stock} Advanced Stock Chart",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=600
        )

        return json.dumps(
            fig,
            cls=plotly.utils.PlotlyJSONEncoder
        )

    except Exception as e:
        print("CHART ERROR:", e)
        return None