from flask import Blueprint, render_template, request, session, redirect, Response
from models.ml_model import predict
from models.db import save_stock, get_history, clear_history
from services.stock_service import fetch, chart
from services.news_service import get_news
from models.nlp_model import analyze_sentiment
import csv


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    price = prediction = accuracy = confidence = signal = None
    sentiment = None
    pos_percent = neg_percent = 0
    graphJSON = error = None

    if request.method == "POST":
        stock = request.form.get("stock")

        if not stock:
            error = "Please enter stock symbol"
        else:
            stock = stock.upper().strip()

            try:
                df = fetch(stock)

                if df is None or df.empty:
                    raise Exception("Invalid stock")

                close_series = df["Close"].dropna()
                last_price = close_series.iloc[-1]

                if hasattr(last_price, "item"):
                    last_price = last_price.item()

                price = round(float(last_price), 2)

                prediction, accuracy, confidence = predict(df)

                if prediction is None or accuracy is None or confidence is None:
                    prediction = price
                    accuracy = 60
                    confidence = 60
                # 📰 Sentiment
                headlines = get_news(stock)
                sentiment, pos_percent, neg_percent = analyze_sentiment(headlines)

                # 📊 Signal
                if prediction > price:
                    signal = "BUY 🚀"
                elif prediction < price:
                    signal = "SELL 🔻"
                else:
                    signal = "HOLD ⚖️"

                # 💾 Save
                save_stock(session["user"], stock, price, prediction, confidence)

                # 📈 Chart
                graphJSON = chart(df, stock)

            except Exception as e:
                print("ERROR:", e)
                error = "Error fetching stock data"

    history = get_history(session["user"])

    return render_template(
        "index.html",
        price=price,
        prediction=prediction,
        accuracy=accuracy,
        confidence=confidence,
        signal=signal,
        sentiment=sentiment,
        pos_percent=pos_percent,
        neg_percent=neg_percent,
        graphJSON=graphJSON,
        history=history,
        error=error
    )


@main.route("/clear", methods=["POST"])
def clear():
    if "user" in session:
        clear_history(session["user"])
    return redirect("/")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/download")
def download():
    if "user" not in session:
        return redirect("/login")

    history = get_history(session["user"])

    def generate():
        data = [["Stock", "Price", "Prediction", "Confidence", "Date"]]

        for row in history:
            data.append([row[0], row[1], row[2], row[3], row[4]])

        for row in data:
            yield ",".join(map(str, row)) + "\n"

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=history.csv"})


# ✅ FIXED ANALYTICS
# =========================
# ANALYTICS DASHBOARD
# =========================
@main.route("/analytics")
def analytics():

    if "user" not in session:
        return redirect("/login")

    history = get_history(session["user"])

    dates = []
    prices = []
    predictions = []

    for row in history:

        dates.append(row[4])

        prices.append(float(row[1]))

        predictions.append(float(row[2]))

    # =========================
    # SENTIMENT
    # =========================
    positive = 0
    negative = 0

    for i in range(len(prices)):

        if predictions[i] > prices[i]:
            positive += 1
        else:
            negative += 1

    if positive == 0 and negative == 0:
        positive = 50
        negative = 50

    sentiment = {
        "positive": positive,
        "negative": negative
    }

    # =========================
    # BETTER ACCURACY
    # =========================
    errors = []

    for i in range(len(prices)):

        actual = prices[i]
        predicted = predictions[i]

        if actual != 0:

            error_percent = abs(actual - predicted) / actual

            errors.append(error_percent)

    if errors:

        avg_error = sum(errors) / len(errors)

        accuracy = max(0, 100 - (avg_error * 100))

        accuracy = round(accuracy, 2)

    else:
        accuracy = 0

    # =========================
    # TREND
    # =========================
    if len(prices) >= 2:

        if prices[-1] > prices[0]:
            trend = "UP 📈"
        else:
            trend = "DOWN 📉"

    else:
        trend = "N/A"

    # =========================
    # ACTIVITY
    # =========================
    if len(history) > 10:
        activity = "High 🔥"

    elif len(history) > 5:
        activity = "Medium ⚡"

    else:
        activity = "Low 💤"

    # =========================
    # RENDER
    # =========================
    return render_template(
        "analytics.html",
        history=history,
        dates=dates,
        prices=prices,
        predictions=predictions,
        sentiment=sentiment,
        accuracy=accuracy,
        trend=trend,
        activity=activity
    )
@main.route("/history")
def history_page():
    if "user" not in session:
        return redirect("/login")

    history = get_history(session["user"])

    return render_template("history.html", history=history)
