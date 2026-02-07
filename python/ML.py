# ============================================================
# CARE LOAD FORECASTING – ML PIPELINE
# Random Forest + ARIMA Comparison
# ============================================================

# ---------------------------
# 1. INSTALL & IMPORT
# ---------------------------

# (Run once in terminal)
# pip install pandas numpy scikit-learn matplotlib openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ---------------------------
# 2. LOAD DATA
# ---------------------------

df = pd.read_csv("UAC_ML_Data.csv")

print("Columns:", df.columns)
print(df.head())


# ---------------------------
# 3. DATE CONVERSION
# ---------------------------

df['Date'] = pd.to_datetime(
    df['Date'],
    format='%d%b%y:%H:%M:%S'
)

df = df.sort_values('Date')


# ---------------------------
# 4. CLEAN TARGET VARIABLE
# ---------------------------

df['Children_in_HHS_Care'] = (
    df['Children_in_HHS_Care']
    .astype(str)
    .str.replace(',', '')
    .astype(float)
)

df['HHS_Care_num'] = df['Children_in_HHS_Care']


# ---------------------------
# 5. FEATURE ENGINEERING
# ---------------------------

# Lag features
df['lag1']  = df['HHS_Care_num'].shift(1)
df['lag7']  = df['HHS_Care_num'].shift(7)
df['lag14'] = df['HHS_Care_num'].shift(14)

# Flow pressure feature
df['net_flow'] = (
    df['Children_transferred_out_of_CBP']
    - df['Children_discharged_from_HHS_Car']
)

# Drop NA rows
df = df.dropna()


# ---------------------------
# 6. TRAIN / TEST SPLIT
# ---------------------------

train = df.iloc[:-30]
test  = df.iloc[-30:]

X_train = train[['lag1','lag7','lag14','net_flow']]
y_train = train['HHS_Care_num']

X_test = test[['lag1','lag7','lag14','net_flow']]
y_test = test['HHS_Care_num']


# ---------------------------
# 7. MODEL TRAINING
# ---------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# ---------------------------
# 8. PREDICTIONS
# ---------------------------

predictions = model.predict(X_test)

test.loc[:, 'ML_Forecast'] = predictions


# ---------------------------
# 9. EVALUATION
# ---------------------------

mae  = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))


# ---------------------------
# 10. VISUALIZATION
# ---------------------------

plt.figure(figsize=(12,6))

plt.plot(test['Date'], y_test, label='Actual')
plt.plot(test['Date'], predictions, label='ML Forecast')

plt.title("Random Forest Care Load Forecast")
plt.xlabel("Date")
plt.ylabel("Children in HHS Care")
plt.legend()
plt.tight_layout()
plt.show()


# ---------------------------
# 11. SAVE ML OUTPUT
# ---------------------------

test.to_csv(
    "ML_Forecast_Output.csv",
    index=False
)

print("ML Forecast file created ✔")


# ============================================================
# 12. ARIMA COMPARISON MERGE
# ============================================================

ml  = pd.read_csv("ML_Forecast_Output.csv")
ari = pd.read_excel("HHS_Forecast (1).xlsx")

# Reset index for alignment
ml  = ml.reset_index(drop=True)
ari = ari.reset_index(drop=True)

# Combine side-by-side
final = pd.concat([ml, ari], axis=1)

# Rename ARIMA columns
final = final.rename(columns={
    'FORECAST': 'ARIMA_Forecast',
    'L95': 'ARIMA_Lower95',
    'U95': 'ARIMA_Upper95'
})

# Save comparison file
final.to_csv(
    "Final_Model_Comparison.csv",
    index=False
)

print("Model comparison file created ✔")
