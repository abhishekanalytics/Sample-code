




from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

data_file = 'data.json'

@app.route('/tasks', methods=['POST', 'GET'])
def manage_tasks():
    try:
        with open(data_file, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []

    if request.method == 'GET':
        # List all tasks
        return jsonify(tasks)
    elif request.method == 'POST':
        # Create a new task
        new_task = request.get_json()
        new_task['id'] = str(uuid.uuid4())
        tasks.append(new_task)

        with open(data_file, 'w') as file:
            json.dump(tasks, file,indent=1)

        return jsonify(new_task)

if __name__ == '__main__':
    app.run(debug=True)



