# Hack-Attack

This project demonstrates an end-to-end fraud detection system with a React frontend, Flask backend, trained machine learning models, and mock data generation.

We designed it as a proof-of-concept to replace third-party fraud detection tools at UPS. Since using real data was not allowed, we generated synthetic shipment logs for 20,000 users across 10 countries, with ~5% fraudulent activity, including:
- **Payment fraud**: shared payment accounts
- **API bashing**: excessive calls in short intervals
- **Location fraud**: inconsistent locales and shipment patterns

## Repository Structure

- **`data/`**: `generate_data.py` to create mock data.
- **`model/`**: Jupyter Notebook to train and export ML models. Tested logistic regression, random forest, and XGBoost; chose XGBoost. Includes feature engineering and encoding.
- **`backend/`**: Flask app (`app.py`) serving REST APIs for predictions and analytics.
- **`frontend/`**: React app with upload page, dashboard, and visualizations.

## Backend
- Built with Flask & `flask_cors`
- Loads trained XGBoost model and encoders
- Processes uploaded CSV logs, performs feature engineering, encodes variables, and predicts fraud
- Endpoints return JSON data for frontend visualizations


### Example Endpoints

| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| POST   | `/upload`           | Upload shipment logs & run predictions |
| GET    | `/summary`          | Return logs, users, fraud counts & rate |
| GET    | `/geography`        | Fraud & non-fraud counts by country |
| GET    | `/time_trends`      | Fraud trends over time by country |
| GET    | `/user_behavior`    | Per-user fraud behavior metrics |
| GET    | `/user_logs/<uuid>` | Logs for a specific user |
| GET    | `/fraud_map`        | Choropleth-ready fraud data |

## Frontend
- Built with React & Material-UI
- Pages: Upload & Dashboard
- Visualizations:
  - Choropleth fraud map (`react-simple-maps`, `d3`)
  - Fraud trends over time with country filter (`chart.js`)
  - Fraud type distribution bar chart
  - Top offenders table
  - User behavior table with option to inspect logs for flagged users
- Communicates with backend via `axios`

## Run the Project

### Clone Repository
```
   git clone https://github.com/2025-UPS-Hackathon/Hack-Attack.git
   cd Hack-Attack
```

### Backend

```
cd backend
pip install -r requirements.txt
python app.py
```
Runs at: http://localhost:5000

### Frontend
```
cd frontend
npm install
npm start
```

Runs at: http://localhost:3000




## Limitations & Future Considerations
-Since real shipment data was unavailable, the model was trained and tested entirely on generated mock data. Training on synthetic data was the best we could do for this proof-of-concept, but we would like to validate and refine the model on real operational data to assess its true effectiveness.

-The current model is binary (fraud/not fraud). With more complex and richer data, we would like to develop a multi-class classification model to detect and distinguish between specific fraud types more accurately.
