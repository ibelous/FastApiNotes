# Running locally

Start the local environment
```bash
docker-compose up
```

Running tests:
```bash
docker-compose run --rm django pytest --cov  # runs them in the containerized environment
# OR
pytest --cov  # runs them on host machine
```


Quality check:
Install pre-commit locally to have your code reformatted before pushing it.


API Schema:
```http://0.0.0.0:8000/docs```
