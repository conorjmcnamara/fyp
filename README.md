# Content-Based Citation Recommendation with Bibliographic Network Awareness

## Running the Application
Set `BACKEND_PORT` and `FRONTEND_PORT` in `/app/.env` to define the ports for the backend API and web application, defaulting to 8000 and 3000, respectively.

### Startup
```sh
cd app
./scripts/startup.sh
```

Once started, the backend API and web application will run in Docker containers and can be accessed at [http://localhost:8000](http://localhost:8000) and [http://localhost:3000](http://localhost:3000), respectively. Additionally, Swagger UI for the API documentation can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs).

### Shutdown
```sh
cd app
./scripts/shutdown.sh
```

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

### Testing
#### Backend
```sh
cd app/backend

pytest
```

After running the tests, a coverage report will be generated and saved at `/app/backend/coverage.xml`.

#### Frontend
```sh
cd app/frontend

npm run test
```

After running the tests, a coverage report will be generated and saved at `/app/frontend/coverage/clover.xml`.