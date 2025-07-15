from flask import Flask, request, jsonify
import pandas as pd
import joblib
import tempfile
import os
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)

model = joblib.load("../fraud_model_xgb.pkl")
le_locale = joblib.load("../locale_encoder.pkl")
le_from = joblib.load("../shipFrom_countryCode_encoder.pkl")
le_to = joblib.load("../shipTo_countryCode_encoder.pkl")

# create a temp file
temp_fd, temp_path = tempfile.mkstemp(suffix='.csv')
os.close(temp_fd)  # Close the open file descriptor

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

    # encoding
    df['locale_enc'] = le_locale.transform(df['locale'])
    df['shipFrom_countryCode_enc'] = le_from.transform(df['shipFrom_countryCode'])
    df['shipTo_countryCode_enc'] = le_to.transform(df['shipTo_countryCode'])

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

    preds = model.predict(X)
    df["prediction"] = preds

    # overwrite the temp file
    df.to_csv(temp_path, index=False)

    return jsonify({"message": "✅ File processed and predictions saved in session."})

@app.route("/summary", methods=["GET"])
def summary():
    df = pd.read_csv(temp_path)

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
    df = pd.read_csv(temp_path)

    # Calculate fraud counts
    fraud_df = (
        df[df["prediction"] == 1]
        .groupby("shipFrom_countryCode")
        .size()
        .reset_index(name="fraud")
    )

    # Calculate not-fraud counts
    not_fraud_df = (
        df[df["prediction"] == 0]
        .groupby("shipFrom_countryCode")
        .size()
        .reset_index(name="not_fraud")
    )

    # Merge fraud and not-fraud counts
    geo = pd.merge(fraud_df, not_fraud_df, on="shipFrom_countryCode", how="outer").fillna(0)

    # Convert counts to integers
    geo["fraud"] = geo["fraud"].astype(int)
    geo["not_fraud"] = geo["not_fraud"].astype(int)

    # Optional: sort by fraud descending
    geo = geo.sort_values(by="fraud", ascending=False)

    return jsonify(geo.to_dict(orient="records"))



@app.route("/time_trends", methods=["GET"])
def time_trends():
    df = pd.read_csv(temp_path)

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
    df = pd.read_csv(temp_path)

    # Aggregate metrics
    behavior = (
        df.groupby('uuid')
        .agg(
            logs=('uuid', 'count'),
            unique_accounts=('payment_accountNumber', 'nunique'),
            frauds=('prediction', 'sum')
        )
        .reset_index()
    )

    # Calculate fraud rate
    behavior['fraud_rate'] = round((behavior['frauds'] / behavior['logs']) * 100, 2)

    # Grab the *first* locale and shipFrom_countryCode per uuid
    extra_cols = df.groupby('uuid').agg(
        locale=('locale', 'first'),
        shipFrom_countryCode=('shipFrom_countryCode', 'first')
    ).reset_index()

    # Merge extra info
    full = pd.merge(behavior, extra_cols, on='uuid', how='left')

    # Optional: sort by most frauds first
    full = full.sort_values(by='frauds', ascending=False)

    return jsonify(full.to_dict(orient="records"))


@app.route("/user_logs/<uuid>", methods=["GET"])
def user_logs(uuid):
    df = pd.read_csv(temp_path)
    user_df = df[df["uuid"] == uuid]

    if user_df.empty:
        return jsonify({"error": f"No logs found for uuid: {uuid}"}), 404

    return jsonify(user_df.to_dict(orient="records"))

@app.route("/fraud_map", methods=["GET"])
def fraud_map():
    df = pd.read_csv(temp_path)

    # static map: code → name
    code_to_name = {
        'US': 'United States of America',
        'DE': 'Germany',
        'AU': 'Australia',
        'FR': 'France',
        'KO': 'South Korea',
        'CA': 'Canada',
        'MX': 'Mexico',
        'KY': 'Cayman Islands',
        'SA': 'Saudi Arabia',
        'MY': 'Malaysia'
    }

    # map to country name
    df['countryName'] = df['shipFrom_countryCode'].map(code_to_name)

    geo = (
        df.groupby('countryName')
        .agg(
            fraud=('prediction', 'sum'),
            total=('prediction', 'count')
        )
        .reset_index()
        .sort_values(by='fraud', ascending=False)
    )

    # create response
    result = []
    for _, row in geo.iterrows():
        result.append({
            "countryName": row["countryName"] or "Unknown",
            "fraud": int(row["fraud"]),
            "total": int(row["total"])
        })

    return jsonify(result)





if __name__ == "__main__":
    app.run(debug=True)
