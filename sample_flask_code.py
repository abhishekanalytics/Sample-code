from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

data_file = 'data.json'

@app.route('/tasks', methods=['POST', 'GET'])
@app.route('/tasks/<task_id>', methods=['PUT', 'DELETE'])
def manage_tasks(task_id=None):
    try:
        with open(data_file, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []

    if request.method == 'GET':
        # here, use List all tasks
        return jsonify(tasks)
    elif request.method == 'POST':
        # here,I create new task
        new_task = request.get_json()
        new_task['id'] = str(uuid.uuid4())
        tasks.append(new_task)

        with open(data_file, 'w') as file:
            json.dump(tasks, file, indent=1)

        return jsonify(new_task)
    elif request.method == 'PUT':
        # Update a task
        if task_id:
            update_data = request.get_json()
            for task in tasks:
                if task['id'] == task_id:
                    task.update(update_data)

                    with open(data_file, 'w') as file:
                        json.dump(tasks, file, indent=1)

                    return jsonify(task)

            return jsonify({"error": "Task not found"})
        else:
            return jsonify({"error": "Task ID not provided in the URL"})
    elif request.method == 'DELETE':
        # Delete a task
        if task_id:
            tasks = [task for task in tasks if task['id'] != task_id]

            with open(data_file, 'w') as file:
                json.dump(tasks, file, indent=1)

            return jsonify({"message": "Task deleted successfully"})
        else:
            return jsonify({"error": "Task ID not provided in the URL"})

if __name__ == '__main__':
    app.run(debug=True)
