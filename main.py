from flask import Flask, jsonify, render_template, request, send_from_directory
from app.database import get_db
from flask_bcrypt import Bcrypt
import project_config
import datetime

user_collection = get_db()
app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html')
   

@app.route('/<page>')
def serve_page(page):
    return send_from_directory('templates', page)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    if user_collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    user_collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully"}), 201


def authenticate_user(username, password):
    user = user_collection.find_one({"username": username})
    if user and bcrypt.check_password_hash(user["password"], password):
        return True
    return False

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = user_collection.find_one({"username": username})
    
    if user and bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not authenticate_user(username, password):
        return jsonify({"message": "Invalid credentials"}), 401

    operation = data.get("operation")
    operand1 = data.get("operand1")
    operand2 = data.get("operand2")

    if operation == "add":
        result = operand1 + operand2
    elif operation == "sub":
        result = operand1 - operand2
    elif operation == "mul":
        result = operand1 * operand2
    elif operation == "div":
        if operand2 == 0:
            return jsonify({"message": "Division by zero is not allowed"}), 400
        result = operand1 / operand2
    else:
        return jsonify({"message": "Invalid operation"}), 400

    history_entry = {
        "username": username,
        "operation": operation,
        "operand1": operand1,
        "operand2": operand2,
        "result": result,
        "timestamp": datetime.datetime.utcnow()
    }
    user_collection.history.insert_one(history_entry)

    return jsonify({"result": result}), 200



@app.route("/history", methods=["POST"])
def history():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not authenticate_user(username, password):
        return jsonify({"message": "Invalid credentials"}), 401

    user_history = list(user_collection.history.find({"username": username}, {"_id": 0,"operation":1,"operand1":1,"operand2":1,"result":1,"timestamp":1}))
    return jsonify(user_history), 200


@app.route("/clear-history", methods=["POST"])
def clear_history():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not authenticate_user(username, password):
        return jsonify({"message": "Invalid credentials"}), 401

    user_collection.history.delete_many({"username": username})
    return jsonify({"message": "History cleared successfully"}), 200

# @app.route('/register', methods = ['POST'])
# def register():
#     user_data = request.form
#     name = user_data.get('name','')
#     username = user_data.get('username', '')
#     password = user_data.get('password','')
#     email_id = user_data.get('email_id','')
#     mobile_number = user_data.get('mobile_number','')
#     dob = user_data.get('dob','')

#     response =  user_collection.find_one({'email_id':email_id})
#     if not response:
#         user_collection.insert_one({"name":name, 'username':username, 'password':password,
#                     'email_id':email_id, 'mobile_number':mobile_number, 'dob':dob})
#         return jsonify({"status": 'Success', "message" :  "User Registerd Successfully"})

#     else:
#         return jsonify({"status": 'Error', "message" :  "User already existy"})

# @app.route('/login', methods = ['POST'])
# def login():
#     user_data = request.form
#     email_id = user_data.get('email_id', '')
#     password = user_data.get('password','')
#     response =  user_collection.find_one({'email_id':email_id,'password':password})
#     if response:
#         return jsonify({"status": 'Success', "message" :  "Login Successful"})
    
#     else:
#         return jsonify({"status": 'Error', "message" :  "Invalid Credentials"})

# @app.route('/forgot', methods = ['POST'])
# def forgot_password():
#     user_data = request.form
#     email_id = user_data.get('email_id', '')
#     dob = user_data.get('dob','')
#     new_password = user_data.get('new_password','')
#     response =  user_collection.find_one({'email_id':email_id,'dob':dob})
#     if response:
#         user_collection.update_one({'email_id':email_id,'dob':dob}, 
#                                    {"$set": {'password':new_password}})
        
#         return jsonify({"status": 'Success', "message" :  "Password updated successfully"})
    
#     else:
#         return jsonify({"status": 'Error', "message" :  "User not exist"})

# @app.route("/calculate", methods=["POST"])
# def calculate():
#     data = request.json
#     username = data["username"]
#     operation = data["operation"]
#     operand1 = float(data["operand1"])
#     operand2 = float(data["operand2"])

#     if operation not in ["add", "sub", "mul", "div"]:
#         return jsonify({"message": "Invalid operation"}), 400

#     result = {
#         "add": operand1 + operand2,
#         "sub": operand1 - operand2,
#         "mul": operand1 * operand2,
#         "div": operand1 / operand2 if operand2 != 0 else None,
#     }[operation]

#     if result is None:
#         return jsonify({"message": "Division by zero is not allowed"}), 400

#     history_entry = {
#         "username": username,
#         "operation": operation,
#         "operand1": operand1,
#         "operand2": operand2,
#         "result": result,
#         "timestamp": datetime.datetime.utcnow(),
#     }
#     user_collection.history_collection.insert_one(history_entry)

#     return jsonify({"result": result}), 200


# @app.route("/history/<username>", methods=["GET"])
# def history(username):
#     history = list(user_collection.history_collection.find({"username": username}, {"_id": 0}))
#     if not history:
#         return jsonify({"Message": "history not found"})
#     else:
#         return jsonify({"history": history}), 200
    

# @app.route("/clear-history/<username>", methods=["DELETE"])
# def clear_history(username):
#     user_collection.history_collection.delete_many({"username": username})
#     return jsonify({"message": "History cleared"}), 200



if __name__ == "__main__":
    app.run(host = '0.0.0.0', port= 8083, debug=True)
    