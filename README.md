# fastapi-backend

This is a test project, that implements an asynchronous API service that:

- Provides an authenticated FastAPI endpoint to query Tao dividends from the Bittensor blockchain
- Caches blockchain query results in Redis for 2 minutes
- Optionally triggers background stake/unstake operations based on Twitter sentiment:
- Queries Twitter via Datura.ai API for tweets about the subnet
- Analyzes tweet sentiment using Chutes.ai LLM
- Stakes or unstakes TAO proportional to sentiment score (-100 to +100)
- Uses Celery workers to handle async blockchain and sentiment analysis tasks
- Stores historical data in a high-concurrency asynchronous database 
 
The architecture follows modern async patterns:
- FastAPI handles HTTP requests
- Redis serves as cache and message broker
- Celery workers process background tasks
- Async database stores results
- Docker containers orchestrate all components


## Usage
1. Clone it `git clone git@github.com:Kulv3r/fast-api-task.git`
1. Do `cp .env_example .env` and update API keys and secrets (if needed) there
1. Run it: `docker-compose up`
1. Do the DB migrations: `docker-compose run --rm backend alembic upgrade head`
1. Check it at GET http://localhost:8000/api/v1/ping
1. Docs:
- http://localhost:8000/redoc - ReDoc
- http://localhost:8000/docs - Swagger
