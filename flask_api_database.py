from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import json

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] ="mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

@app.route('/tasks', methods=['POST', 'GET'])
@app.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_tasks(task_id=None):
    try:
        tasks_collection = mongo.db.tasks

        if request.method == 'GET':
            if task_id:
                # Get a single task by ID
                task = tasks_collection.find_one({'_id': ObjectId(task_id)})
                if task:
                    #here I am  Converting  ObjectId to string (for JSON serialization)
                    task['_id'] = str(task['_id'])
                    return jsonify(task)
                else:
                    return jsonify({"error": "Task not found"})
            else:
                # This is for List all tasks
                tasks = list(tasks_collection.find())
                # Convert ObjectId to string for JSON serialization
                for task in tasks:
                    task['_id'] = str(task['_id'])
                return jsonify(tasks)
        elif request.method == 'POST':
            # Create a new task
            new_task = request.get_json()
            new_task['_id'] = ObjectId()
            tasks_collection.insert_one(new_task)

            # Convert ObjectId to string for JSON serialization
            new_task['_id'] = str(new_task['_id'])
            return jsonify(new_task)
        

        elif request.method == 'PUT':
            # Update a task
            if task_id:
                update_data = request.get_json()
                result = tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': update_data})

                if result.modified_count > 0:
                    updated_task = tasks_collection.find_one({'_id': ObjectId(task_id)})

                    # Convert ObjectId to string for JSON serialization
                    
                    updated_task['_id'] = str(updated_task['_id'])
                    return jsonify(updated_task)
                else:
                    return jsonify({"error": "Task not found"})
            else:
                return jsonify({"error": "Task ID not provided in the URL"})
        elif request.method == 'DELETE':
            # Delete a task
            if task_id:
                result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
                if result.deleted_count > 0:
                    return jsonify({"message": "Task deleted successfully"})
                else:
                    return jsonify({"error": "Task not found"})
            else:
                return jsonify({"error": "Task ID not provided in the URL"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)