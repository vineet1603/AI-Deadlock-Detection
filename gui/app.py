from flask import Flask, request, render_template, jsonify
import joblib

app = Flask(__name__)

# Load the trained deadlock detection model
model = joblib.load("/home/kali/AI_Deadlock_Detection/gui/deadlock_detector.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            process_id = int(request.form["process_id"])
            resource_id = int(request.form["resource_id"])
            wait_time = int(request.form["wait_time"])

            # Predict deadlock
            prediction = model.predict([[process_id, resource_id, wait_time]])[0]
            result = "Deadlock Detected! 🚨" if prediction == 1 else "No Deadlock 😊"

            return render_template("index.html", result=result)
        except Exception as e:
            return render_template("index.html", result=f"Error: {str(e)}")
    return render_template("index.html", result="")

if __name__ == "__main__":
    app.run(debug=True)

