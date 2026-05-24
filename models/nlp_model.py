from textblob import TextBlob

def analyze_sentiment(headlines):
    try:
        if not headlines:
            return "No News ⚪", 0

        pos = 0
        neg = 0
        neutral = 0

        for headline in headlines:
            score = TextBlob(headline).sentiment.polarity

            if score > 0.3:
                pos += 1
            elif score < -0.3:
                neg += 1
            else:
                neutral += 1

        total = pos + neg + neutral

        # 📊 Calculate percentage
        pos_percent = round((pos / total) * 100, 2)
        neg_percent = round((neg / total) * 100, 2)

        # 🧠 Final sentiment label
        if pos > neg and pos > neutral:
            sentiment = "Positive 🟢"
        elif neg > pos and neg > neutral:
            sentiment = "Negative 🔴"
        else:
            sentiment = "Neutral 🟡"

        return sentiment, pos_percent, neg_percent

    except Exception as e:
        print("NLP ERROR:", e)
        return "Neutral 🟡", 0, 0