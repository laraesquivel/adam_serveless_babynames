# Babys Names API Recommender

## Running Locally


### With Docker

```bash
# Build the Docker image
docker build -t adam_serveless_babynames .

# Run the Docker container
docker run -p 8000:8000 adam_serveless_babynames

```

### With uvicorn

#### Install dependencies

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Your FastApi application is now available at `http://localhost:8000`.