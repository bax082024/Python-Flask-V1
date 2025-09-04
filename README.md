# Tiny Flask API

- Made for fun to test basic curl commands on a flask API.

## Commands:

- **Health:**
  - curl http://127.0.0.1:8000/api/health

- **list tasks**
  - curl http://127.0.0.1:8000/api/tasks

- **filter:**
  - curl "http://127.0.0.1:8000/api/tasks?done=true"

- **create:**
  - curl -X POST http://127.0.0.1:8000/api/tasks \
      -H "Content-Type: application/json" \
      -d '{"title": "replace with title you want"}'

- **update:**
  - curl -X PATCH http://127.0.0.1:8000/api/tasks/1 \
    -H "Content-Type: application/json" \
    -d '{"done": true}'


## Deps

- pip install Flask flask-cors python-dotenv

- pip freeze > requirements.txt
