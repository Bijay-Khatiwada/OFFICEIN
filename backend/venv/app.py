from flask import Flask, jsonify,  render_template, make_response, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client.bizDB # select the database
employees = db.fake_employees # selecst the collection 

@app.route("/employees", methods=["GET"])
def show_all_fake_employees():
   page_num, page_size = 1, 10
   if request.args.get('pn'):
      page_num = int(request.args.get('pn'))

   if request.args.get('ps'):
      page_size = int(request.args.get('ps'))
   
   page_start = (page_size * (page_num - 1))

   data_to_return = []
   cursor = employees.find().skip(page_start).limit(page_size)
   
   for employee in cursor:
        # Convert ObjectId to string for JSON serialization
        employee['_id'] = str(employee['_id'])
        data_to_return.append(employee)
   return make_response( jsonify(data_to_return), 200 )    


@app.route("/employee/<string:id>", methods=["GET"])
def show_one_employee(id):
    employee = employees.find_one({'_id': ObjectId(id)})
    if employee is not None:
        employee['_id'] = str(employee['_id'])
        return make_response(jsonify([employee]), 200)
    else:
        return make_response(jsonify({"error": "Invalid employee ID"}), 404)
@app.route('/addEmployee', methods=['POST'])
def add_data():
    data = request.get_json()  # Assuming data is sent as JSON in the request body
    
    # Extract fields from JSON data
    name = data.get('name')
    email = data.get('email')
    position = data.get('position')
    age = data.get('age')

    # Create a document to insert into MongoDB
    new_record = {
        'name': name,
        'email': email,
        'position': position,
        'age': age
    }

    # Insert the document into the MongoDB collection
    result = employees.insert_one(new_record)

    # Prepare a response
    response = {
        'message': 'Data added successfully',
        'inserted_id': str(result.inserted_id)  # Convert ObjectId to string
    }

    return jsonify(response), 201  # Respond with HTTP status code 201 (Created)


@app.route("/employee-del/<string:id>", methods=["DELETE"])
def delete_employee(id):
    result = employees.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid task ID"}), 404)


@app.route("/update-employee/<string:id>", methods=["PUT"])
def edit_task(id):
    required_fields = ["name", "email", "age", "position"]
    if all(field in request.json for field in required_fields):
        result = employees.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.json["name"],
                "age": request.json["age"],
                "email": request.json["email"],
                "position": request.json["position"],
            }}
        )
        if result.matched_count == 1:
            edited_link = "http://localhost:5000/employees/" + id
            return make_response(jsonify({"url": edited_link}), 200)
        else:
            return make_response(jsonify({"error": "Invalid ID"}), 404)
    else:
        return make_response(jsonify({"error": "Missing form data"}), 400)

if __name__ == "__main__":
    app.run(debug=True)