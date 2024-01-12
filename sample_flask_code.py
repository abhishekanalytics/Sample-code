
from flask import Flask,request,jsonify
import json 
import os

app=Flask(__name__)

data_file='data.json'

try:
     with open(data_file, 'r') as file:
        tasks = json.load(file)
            
except FileNotFoundError:
    with open(data_file, 'w') as file:
     tasks = []
     json.dump(tasks, file)

@app.route('/www.files.com/', methods=['GET'])
def get_tasks():
    try:
        with open(data_file, 'r') as file:
            tasks = json.load(file)
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/www.files.com/', methods=['POST'])
def create_task():
    try:
        new_task = request.get_json()

        with open(data_file, 'r') as file:
            tasks = json.load(file)

        new_task['id'] = len(tasks) + 1
        tasks.append(new_task)

        with open(data_file, 'w') as file:
            json.dump(tasks, file, indent=2)

        return jsonify(new_task), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500   

@app.route('/www.files.com/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        with open(data_file, 'r') as file:
            tasks = json.load(file)
            task = next((t for t in tasks if t['id'] == task_id), None)
            if task:
                return jsonify(task)
            else:
                return jsonify({"error": "Task not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
if __name__ == '__main__':
    app.run(debug=True)