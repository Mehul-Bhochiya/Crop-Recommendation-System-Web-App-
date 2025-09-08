import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")
X = df.drop(columns=["Crop"])
y = df["Crop"]

# Scale: StandardScaler -> MinMaxScaler
sc = StandardScaler()
X_scaled = sc.fit_transform(X)

ms = MinMaxScaler()
X_final = ms.fit_transform(X_scaled)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Model training with class balancing
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    min_samples_split=4,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model and scalers as a single object
package = {
    'model': model,
    'standard_scaler': sc,
    'minmax_scaler': ms
}

with open("model.pkl", "wb") as f:
    pickle.dump(package, f)

print("Model and scalers saved to model.pkl")
