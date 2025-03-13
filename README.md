# pytest-clean-database example project
An example project to showcase the usage of pytest-clean-database. Built using FastAPI, 
asyncpg (for PostgreSQL), mysql-connector-python (for MySQL).

# Usage
Requires Python >=3.8 and Docker Compose.

1. Clone the repository.
2. Run `cd pytest-clean-database-example`.
3. Run `docker compose up -d` to start both database servers.
4. Run `python -m venv venv && source venv/bin/activate && pip install -r
   requirements.txt` to create a virtual environment and install dependencies.

To run tests using pytest-clean-database just run `pytest --asyncio-mode auto`. All tests 
should pass.

To run tests without pytest-clean-database run `pytest -p no:clean-db --asyncio-mode auto`. 
The tests should fail due to a lack of isolation between test cases.

Note that this repository has two branches, `main` and `mysql`. Switch between them to 
see PostgreSQL/MySQL variants.
