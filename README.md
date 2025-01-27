# Content-Based Citation Recommendation with Bibliographic Network Awareness
## Running the Research
The Jupyter notebooks in `research/notebooks` contain the entrypoints for all experiments.

### Installation
Each notebook contains dependency installation commands.

```sh
cd research/requirements

pip install -r base.txt
pip install -r dev.txt
```

### Linting
```sh
cd research

flake8 .
```

## Running the Application
### Installation
#### Backend
```sh
cd app/backend/requirements

pip install -r base.txt
pip install -r dev.txt
```

#### Frontend
```sh
cd app/frontend

npm install
```

### Docker
Define the ports for the backend API and web application by setting `BACKEND_PORT` and `FRONTEND_PORT` in `app/.env`, defaulting to 8000 and 3000, respectively.

#### Startup
```sh
cd app

./scripts/startup.sh
```

Once started, the backend API and web application will run in Docker containers and can be accessed at [http://localhost:8000](http://localhost:8000) and [http://localhost:3000](http://localhost:3000), respectively. Additionally, Swagger UI for the API documentation can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs).

#### Shutdown
```sh
cd app

./scripts/shutdown.sh
```

### Testing
#### Backend
```sh
cd app/backend

pytest
```

After running the tests, a coverage report will be generated and saved at `app/backend/coverage.xml`.

#### Frontend
```sh
cd app/frontend

npm run test
```

After running the tests, a coverage report will be generated and saved at `app/frontend/coverage/clover.xml`.

### Linting
#### Backend
```sh
cd app/backend

flake8 .
```

#### Frontend
```sh
cd app/frontend

npm run lint
```