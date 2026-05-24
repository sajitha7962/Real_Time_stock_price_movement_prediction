from xgboost import XGBRegressor
import numpy as np
from sklearn.metrics import mean_absolute_error

def predict(df):

    try:
        # =========================
        # FEATURES
        # =========================
        features = [
            "Open",
            "High",
            "Low",
            "Volume",
            "SMA_10",
            "EMA_10",
            "RSI",
            "MACD",
            "BB_HIGH",
            "BB_LOW"
        ]

        df = df.dropna()

        if len(df) < 40:
            return None, None, None

        X = df[features]
        y = df["Close"].values

        # =========================
        # TRAIN TEST SPLIT
        # =========================
        split = int(len(df) * 0.8)

        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        # =========================
        # MODEL
        # =========================
        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )

        model.fit(X_train, y_train)

        # =========================
        # PREDICTION
        # =========================
        y_pred = model.predict(X_test)

        # =========================
        # 1. REALISTIC ACCURACY (DIRECTIONAL)
        # =========================
        correct = 0
        total = len(y_test)

        for i in range(1, total):
            actual_direction = y_test[i] - y_test[i - 1]
            pred_direction = y_pred[i] - y_pred[i - 1]

            if (actual_direction > 0 and pred_direction > 0) or \
               (actual_direction < 0 and pred_direction < 0):
                correct += 1

        accuracy = (correct / (total - 1)) * 100 if total > 1 else 0

        # =========================
        # 2. REALISTIC CONFIDENCE
        # =========================
        # =========================
# 2. CONSISTENT CONFIDENCE SCORE (REALISTIC SCALE)
# =========================
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))

        avg_price = np.mean(y_test)

        error_score = (mae + rmse) / (2 * avg_price)

# smooth bounded sigmoid-style mapping
        confidence = 100 * (1 / (1 + np.exp(10 * (error_score - 0.05))))

# optional soft clamp (not hard lock)
        confidence = np.clip(confidence, 40, 95)
        # =========================
        # 3. NEXT DAY PREDICTION
        # =========================
        latest_data = X.iloc[-1:].values
        prediction = float(model.predict(latest_data)[0])

        return (
            round(prediction, 2),
            round(float(accuracy), 2),
            round(float(confidence), 2)
        )

    except Exception as e:
        print("ML ERROR:", e)
        return None, None, None