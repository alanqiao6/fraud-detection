from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # if React runs on localhost:3000

model = joblib.load("../fraud_model_xgb.pkl")

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

    result = df[["uuid", "prediction"]].to_dict(orient="records")
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
