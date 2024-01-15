from flask import Flask, request, jsonify
import json
import os
import uuid

app = Flask(__name__)

data_file = 'data.json'

@app.route('/tasks', methods=['POST', 'GET', 'PUT', 'DELETE'])
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
        # Here,Create a new task
        new_task = request.get_json()
        new_task['id'] = str(uuid.uuid4())
        tasks.append(new_task)

        with open(data_file, 'w') as file:
            json.dump(tasks, file, indent=1)

        return jsonify(new_task)
    elif request.method == 'PUT':
        #  Here,Update a task
        task_id_to_update = request.args.get('id')
        update_data = request.get_json()
        print("DASDSDFDSFD")
        for task in tasks:
            print("ASASASAS")
            print(task['id'],task_id_to_update)

            if task['id'] == task_id_to_update:
                task.update(update_data)

                with open(data_file, 'w') as file:
                    json.dump(tasks, file, indent=1)

                return jsonify(task)

        return jsonify({"error": "Task not found"})
    

    elif request.method == 'DELETE':
        # Here,Delete a task
        task_id_to_delete = request.args.get('id')

        tasks = [task for task in tasks if task['id'] != task_id_to_delete]

        with open(data_file, 'w') as file:
            json.dump(tasks, file, indent=1)

        return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':

    app.run(debug=True)




