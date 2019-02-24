from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# client = PyMongo.MongoClient()
# db = client.mars_db
# collection = db.mars_facts


@app.route('/')
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template('mars_index.html', mars_info=mars_info)


# Route that will trigger the scrape function
@app.route('/scrape')
def scrapper():
    mars_info = mongo.db.mars_info
    data = scrape_mars.scrape()
    mars_info.update({}, data, upsert=True)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)