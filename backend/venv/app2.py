from flask import Flask, jsonify,  render_template, make_response, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.bizDB # select the database
employees = db.fake_employees# selecst the collection 



@app.route("/")
def get_document_count():
    cursor = list(employees.find())
    document_count = len(cursor) # Get the count of documents in the collection
    return f"Number of documents: {document_count}"


if __name__ == "__main__":
    app.run(debug=True)
