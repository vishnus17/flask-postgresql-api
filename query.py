from os import times
from re import S
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
import schedule
import time
import sqlite3 as sl
from flask_apscheduler import APScheduler

app = Flask(__name__)
# scheduler=APScheduler()

engine = create_engine("postgresql://postgres:vava@localhost:5432/mydb", pool_size=10, max_overflow=20)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vava@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class People(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    age = db.Column(db.String(120), nullable=False)

    def __init__(self, name, age):
        self.name = name
        self.age = age
              

#Adding data into db
@app.route("/")
def addperson():
    return render_template("data.html")

@app.route("/add", methods=['POST'])
def add():
    name = request.form["name"]
    age = request.form["age"]
    entry = People(name, age)
    db.session.add(entry)
    db.session.commit()
    return {"message": f"name {entry.name} has been added successfully."}


#Taking query from user using form
@app.route("/query", methods=['POST','GET'])
def query():
    return render_template("index.html")

@app.route("/queryresult", methods=['POST'])
def queryresult():
    # times=request.form['time']
    try:
        result= db.engine.execute(request.form['query'])
        queryout = {}
        i=1
        for each in result:
            queryout.update({f'{i}': list(each)})
            i+=1
        return {"Query executed successfully": f"{queryout} "}
    except:
        return {"Error": "Request could not be completed. Please enter correct SELECT statement"}

  
#execute query from user using postman
@app.route('/execute', methods=['POST'])
def execute():
    try:
        db.engine.execute(request.get_json()['query'])
    except:
        return {"message": "Request could not be completed."}
  
    return {"message": "Query executed successfully."}

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


    # scheduler.add_job(id= 'query result',func = queryresult,trigger='interval', seconds=5 )
    # scheduler.start()

    # schedule.every().day.at(times).do(queryresult)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)