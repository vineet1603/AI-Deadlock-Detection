import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Simulated dataset: CPU usage, I/O wait, Lock Requests
data = np.array([[1, 2, 2], [2, 3, 3], [3, 2, 1], [4, 5, 6], [3, 3, 3]])
labels = np.array([0, 1, 0, 1, 1])  # 0 = No Deadlock, 1 = Deadlock

# Train the model
clf = RandomForestClassifier()
clf.fit(data, labels)

# Save model
joblib.dump(clf, "ai_model/deadlock_model.pkl")

def predict_deadlock(features):
    """Predict if the system is in a deadlock-prone state."""
    clf = joblib.load("ai_model/deadlock_model.pkl")
    return clf.predict([features])

if __name__ == "__main__":
    test_data = [2, 3, 2]  # Example input
    print("Deadlock risk:", predict_deadlock(test_data))
