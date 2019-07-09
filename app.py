#Import Dependencies
import os
import pandas as pd
# import numpy as np
# from random import sample
# from pandas import DataFrame

import pymongo
from pymongo import MongoClient

from flask_pymongo import PyMongo
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Connection for Heroku - Will work locally
# app.config["MONGO_DBNAME"] = 'clorec_db'
# app.config["MONGO_URI"] = "mongodb+srv://thidar:mongoexplorer2019@city-explorer-ocvlm.mongodb.net/clorec_db"
mongo = PyMongo(app, uri = "mongodb+srv://thidar:mongoexplorer2019@city-explorer-ocvlm.mongodb.net/clorec_db")
db = mongo.db

# Setup local connection
# connect = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(connect)
# db = client.clorec_db

c_users = db.user_details

# Retrieve user details from MongoDB
user_details = list(c_users.find({}, {'_id': 0}))
user_details_df = pd.DataFrame(user_details)

########### RENDER HTML routes #############
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/data_overview")
def data_overview():
    return render_template("data_overview.html")

@app.route("/models_overview")
def models_overview():
    return render_template("models_overview.html")

@app.route("/models/<user>")
def updatePhoto(user):
    print(user)
    userData = user_details_df.loc[user_details_df['reviewerID']==int(user)]
    data = userData.to_dict("records")
    return render_template("models_analysis.html", photos=data)


@app.route("/models_analysis")
def models_analysis():
    return render_template("models_analysis.html")

@app.route("/models_plot")
def models_plot():
    return render_template("models_plot.html")

@app.route("/rec-models")
def rec_models():
    return render_template("rec-models.html")

@app.route("/sentiment_analysis")
def sentiment_analysis():
    return render_template("sentiment_analysis.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/overall-rating")
def overall_rating():
    return render_template("overall-rating.html")

@app.route("/rate-scatter")
def rate_scatter():
    return render_template("rate-scatter.html")

@app.route("/word-scatter")
def word_scatter():
    return render_template("word-scatter.html")

@app.route("/reviews-over-time")
def reviews_over_time():
    return render_template("reviews-over-time.html")

@app.route("/sentiment-results")
def sentiment_results():
    return render_template("sentiment-results.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/users")
def users():
    return jsonify(user_details)

if __name__ == '__main__':
    #app.run(debug=False)
    port = int(os.environ.get("PORT", 5000)) 
    app.run(debug=False, host='0.0.0.0', port=port)