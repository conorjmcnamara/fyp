# Content-Based Citation Recommendation with Bibliographic Network Awareness
## Running the Research
### Installation
```sh
cd research/requirements

pip install -r requirements.txt
```

Notebooks that require additional dependencies include the necessary installation commands.

To install development dependencies (for linting), run:

```sh
cd research/requirements

pip install -r requirements.dev.txt
```

### Usage
The Jupyter notebooks in `research/notebooks` contain the entrypoints for all experiments.

#### GPU Acceleration
For optimal performance, it is recommended to run the following tasks in a GPU-enabled environment (such as Google Colab):
- `research/notebooks/rq1.ipynb`: SciBERT text embedding generation
- `research/notebooks/rq2.ipynb`: SPECTER and SPECTER2 text embedding generation

#### Linting
```sh
cd research

flake8 .
```

## Running the Application
### Installation
Copy the `.env.example` files to `.env` in the `app/backend` and `app/frontend` directories:

```sh
cp app/backend/.env.example app/backend/.env

cp app/frontend/.env.example app/frontend/.env
```

#### Backend
```sh
cd app/backend/requirements

pip install -r requirements.txt
```

To install development dependencies (for linting and testing), run:

```sh
cd app/backend/requirements

pip install -r requirements.dev.txt
```

#### Database
Set the `DATABASE_URL` environment variable in `app/backend/.env`. Then, run the following script to populate the database with papers:

```sh
cd app/backend

python -m src.utils.populate_db <path_to_papers_json_file>
```

#### Frontend
```sh
cd app/frontend

npm install
```

### Usage
Set the `BACKEND_PORT` and `FRONTEND_URL` environment variables in `app/backend/.env`, and `FRONTEND_PORT` and `BACKEND_URL` environment variables in `app/frontend/.env`.

#### Docker
##### Startup
```sh
cd app

./scripts/startup.sh
```

Once started, the backend API and web application will run in Docker containers and can be accessed at [http://localhost:8000](http://localhost:8000) and [http://localhost:3000](http://localhost:3000), respectively. Additionally, Swagger UI for the API documentation can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs).

##### Shutdown
```sh
cd app

./scripts/shutdown.sh
```

#### Local
##### Backend
```sh
cd app/backend

python -m src.main
```

##### Frontend
```sh
cd app/frontend

npm start
```

#### Testing
##### Backend
```sh
cd app/backend

pytest
```

After running the tests, a coverage report will be generated and saved at `app/backend/coverage.xml`.

##### Frontend
```sh
cd app/frontend

npm run test
```

After running the tests, a coverage report will be generated and saved at `app/frontend/coverage/clover.xml`.

#### Linting
##### Backend
```sh
cd app/backend

flake8 .
```

##### Frontend
```sh
cd app/frontend

npm run lint
```