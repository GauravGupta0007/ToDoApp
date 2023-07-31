from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

#setting up the data base
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos

#Model
class Task(db.Model):
    task_no = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String, nullable = True)
    created_date = db.Column(db.DateTime, default = datetime.now(), nullable = False)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String, default = "In-Progress", nullable = False)    

    def __repr__(self):
        return self.task

@app.route("/")
def list_tasks():
    tasks = Task.query.all()
    return render_template("index.html", tsk = tasks)

@app.route("/add", methods = ["GET", "POST"])
def create_task():
    if request.method == "POST":
        task = Task(task = request.form["task"], due_date = datetime.fromisoformat(request.form["due_date"], status = request.form["status"]))
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:no>", methods = ["GET", "POST"])
def edit_task(no):
    print(no)
    return render_template("edit.html")

@app.route("/delete/<int:no>")
def delete_task(no):
    print(no)
    return redirect("/")

app.run(debug = True)