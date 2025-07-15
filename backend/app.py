from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # if React runs on localhost:3000

model = joblib.load("../fraud_model_xgb.pkl")
PREDICTIONS_FILE = "latest_predictions.csv"


@app.route("/")
def home():
    return "✅ Fraud Detection API is running! Use POST /upload to send a log file."

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    # feature engineering
    df['shipFrom_differs_from_locale'] = (df['shipFrom_countryCode'] != df['locale']).astype(int)
    df['is_domestic'] = (df['shipFrom_countryCode'] == df['shipTo_countryCode']).astype(int)
    df['shipment_datetime'] = pd.to_datetime(df['ship_date'] + ' ' + df['ship_time'])
    df.sort_values(by=['uuid', 'shipment_datetime'], inplace=True)
    df['time_delta_minutes'] = df.groupby('uuid')['shipment_datetime'].diff().dt.total_seconds() / 60
    df['time_delta_minutes'].fillna(-1, inplace=True)
    df['num_users_per_account'] = df.groupby('payment_accountNumber')['uuid'].transform('nunique')

    # load encoders
    le_locale = joblib.load("../locale_encoder.pkl")
    le_from = joblib.load("../shipFrom_countryCode_encoder.pkl")
    le_to = joblib.load("../shipTo_countryCode_encoder.pkl")

    # apply encoders
    df['locale_enc'] = le_locale.transform(df['locale'])
    df['shipFrom_countryCode_enc'] = le_from.transform(df['shipFrom_countryCode'])
    df['shipTo_countryCode_enc'] = le_to.transform(df['shipTo_countryCode'])

    # select features
    feature_cols = [
        'shipFrom_differs_from_locale',
        'is_domestic',
        'time_delta_minutes',
        'num_users_per_account',
        'locale_enc',
        'shipFrom_countryCode_enc',
        'shipTo_countryCode_enc'
    ]
    X = df[feature_cols]

    # predict
    preds = model.predict(X)
    df["prediction"] = preds

    df.to_csv(PREDICTIONS_FILE, index=False)
    return jsonify({"message": "✅ File processed and predictions saved."})

@app.route("/summary", methods=["GET"])
def summary():
    df = pd.read_csv(PREDICTIONS_FILE)

    total_logs = len(df)
    total_users = df['uuid'].nunique()
    fraud_count = (df['prediction'] == 1).sum()
    not_fraud_count = (df['prediction'] == 0).sum()
    fraud_rate = round((fraud_count / total_logs) * 100, 2)

    return jsonify({
        "total_logs": total_logs,
        "total_users": total_users,
        "fraud": int(fraud_count),
        "not_fraud": int(not_fraud_count),
        "fraud_rate": fraud_rate
    })

@app.route("/geography", methods=["GET"])
def geography():
    df = pd.read_csv(PREDICTIONS_FILE)

    geo = (
        df.groupby('shipFrom_countryCode')['prediction']
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={0: "not_fraud", 1: "fraud"})
    )

    return jsonify(geo.to_dict(orient="records"))


@app.route("/time_trends", methods=["GET"])
def time_trends():
    df = pd.read_csv(PREDICTIONS_FILE)

    df['shipment_datetime'] = pd.to_datetime(df['ship_date'] + ' ' + df['ship_time'])
    df['date'] = df['shipment_datetime'].dt.date

    trends = (
        df.groupby('date')['prediction']
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={0: "not_fraud", 1: "fraud"})
        .sort_values("date")
    )

    return jsonify(trends.to_dict(orient="records"))


@app.route("/user_behavior", methods=["GET"])
def user_behavior():
    df = pd.read_csv(PREDICTIONS_FILE)

    behavior = (
        df.groupby('uuid')
        .agg(
            logs=('uuid', 'count'),
            unique_accounts=('payment_accountNumber', 'nunique'),
            frauds=('prediction', 'sum')
        )
        .reset_index()
    )

    behavior['fraud_rate'] = round((behavior['frauds'] / behavior['logs']) * 100, 2)

    return jsonify(behavior.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
