from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/attendance", methods=["POST"])
def attendance():
    # Get the user and class data from the request
    user = request.form["user"]
    class_name = request.form["class_name"]
    time = request.form["time"]

    # Check if the user is logged in
    if user not in session:
        return "You must be logged in to record attendance."

    # Save the attendance data to a file
    with open("attendance.json", "r") as f:
        attendance_data = json.load(f)

    attendance_data[user] = {
        "class_name": class_name,
        "time": time
    }

    with open("attendance.json", "w") as f:
        json.dump(attendance_data, f)

    return redirect("/")

@app.route("/search", methods=["POST"])
def search():
    # Get the user name from the request
    user = request.form["user"]

    # Check if the user is logged in
    if user not in session:
        return "You must be logged in to search for attendance."

    # Get the attendance data from the file
    with open("attendance.json", "r") as f:
        attendance_data = json.load(f)

    if user in attendance_data:
        classes = attendance_data[user]["class_name"]
        times = attendance_data[user]["time"]

        return render_template("search.html", user=user, classes=classes, times=times)
    else:
        return "No attendance data found for user {}".format(user)

@app.route("/login", methods=["POST"])
def login():
    # Get the user name and password from the request
    user = request.form["user"]
    password = request.form["password"]

    # Check if the user name and password are correct
    if user == "stpiusx" and password == "beverton":
        session["user"] = user
        return redirect("/")
    else:
        return "Invalid username or password."

@app.route("/logout")
def logout():
    # Clear the user session
    session.clear()
    return redirect("/")

@app.template_folder("templates")
def template_folder():
    return "templates"

if __name__ == "__main__":
    app.run(debug=True)
