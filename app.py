from flask import Flask, request, jsonify, redirect
import os

app = Flask(__name__)

@app.route('/data')
def redirect_forever():
    return redirect('/data')  # Redirect to itself

@app.route('/', methods=['GET'])
def hello():
    for k, v in request.headers:
        print(f"{k}: {v}")
    return "okk"

@app.route('/', methods=['POST'])
def data():
    print("*** data: ", request.form)
    for k, v in request.headers:
        print(f"{k}: {v}")
    return request.form

@app.route('/', methods=['PUT'])
def update_data():
    # Handling PUT request
    print("*** PUT data: ", request.form)
    for k, v in request.headers:
        print(f"{k}: {v}")
    return jsonify(message="Data updated", data=request.form)

@app.route('/', methods=['DELETE'])
def delete_data():
    # Handling DELETE request
    for k, v in request.headers:
        print(f"{k}: {v}")
    return jsonify(message="Data deleted")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
