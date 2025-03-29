import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Create a sample dataset (replace with actual system logs)
data = pd.DataFrame({
    "process_id": [1, 2, 3, 4, 5, 6],
    "resource_id": [10, 20, 10, 30, 20, 10],
    "wait_time": [5, 15, 25, 35, 45, 55],
    "is_deadlocked": [0, 1, 0, 1, 0, 1]
})

X = data[['process_id', 'resource_id', 'wait_time']]
y = data['is_deadlocked']

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "deadlock_detector.pkl")

print("✅ Model trained and saved as 'deadlock_detector.pkl'")
