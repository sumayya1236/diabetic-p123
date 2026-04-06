from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Login Page
@app.route("/")
def index():
    return render_template("login.html")

# Login verification
@app.route("/login", methods=["POST"])
def login():

    uname = request.form["uname"]
    pwd = request.form["pwd"]

    if uname == "admin" and pwd == "admin":
        return render_template("homepage.html")
    else:
        return render_template("login.html", result="Invalid Username or Password")


# Prediction
@app.route("/predict", methods=["POST"])
def predict():

    age = float(request.form["age"])
    bmi = float(request.form["bmi"])
    preg = float(request.form["preg"])
    bp = float(request.form["bp"])
    glu = float(request.form["glu"])
    family = float(request.form["family"])

    data = [age, bmi, preg, bp, glu, family]

    pred = model.predict([data])

    # Risk Score Calculation
    score = 0

    if age >= 30:
        score += 2
    if bmi >= 25:
        score += 2
    if preg >= 3:
        score += 1
    if bp >= 140:
        score += 1
    if glu >= 140:
        score += 3
    if family == 1:
        score += 1

    # Risk Level
    if score <= 3:
        risklevel = "Low Risk"
    elif score <= 6:
        risklevel = "Moderate Risk"
    else:
        risklevel = "High Risk"

    if pred[0] == 1:
        result = "Diabetes Risk Detected"
    else:
        result = "No Diabetes Risk"

    return render_template(
        "homepage.html",
        result=result,
        riskscore=score,
        risklevel=risklevel
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
