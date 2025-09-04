import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow requests from your frontend during development

# simple in-memory store (swap with a DB later)
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build an API", "done": True},
]

# helpers
def next_id():
    return max((t["id"] for t in tasks), default=0) + 1

def bad_request(msg):
    return jsonify({"error": msg}), 400

# health check
@app.get("/api/health")
def health():
    return jsonify(status="ok")

# list tasks (supports ?done=true/false)
@app.get("/api/tasks")
def list_tasks():
    done = request.args.get("done")
    data = tasks
    if done is not None:
        if done.lower() not in {"true", "false"}:
            return bad_request("done must be true or false")
        want = done.lower() == "true"
        data = [t for t in tasks if t["done"] == want]
    return jsonify(data)

# get one task
@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "not found"}), 404
    return jsonify(task)

# create task
@app.post("/api/tasks")
def create_task():
    body = request.get_json(silent=True) or {}
    title = body.get("title")
    if not title or not isinstance(title, str):
        return bad_request("title (string) is required")
    task = {"id": next_id(), "title": title.strip(), "done": False}
    tasks.append(task)
    return jsonify(task), 201

# update task (PUT = full update; PATCH = partial)
@app.put("/api/tasks/<int:task_id>")
@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "not found"}), 404

    body = request.get_json(silent=True) or {}
    if request.method == "PUT":
        # require both fields
        if "title" not in body or "done" not in body:
            return bad_request("PUT requires title and done")
        if not isinstance(body["title"], str) or not isinstance(body["done"], bool):
            return bad_request("title must be string; done must be boolean")
        task["title"] = body["title"].strip()
        task["done"] = body["done"]
    else:  # PATCH
        if "title" in body:
            if not isinstance(body["title"], str):
                return bad_request("title must be string")
            task["title"] = body["title"].strip()
        if "done" in body:
            if not isinstance(body["done"], bool):
                return bad_request("done must be boolean")
            task["done"] = body["done"]

    return jsonify(task)

# delete task
@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    idx = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    if idx is None:
        return jsonify({"error": "not found"}), 404
    tasks.pop(idx)
    return "", 204

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
