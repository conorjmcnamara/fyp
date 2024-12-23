# Final Year Project

## Running the Application
Set `BACKEND_PORT` and `FRONTEND_PORT` in `/app/.env` to define the ports for the backend API and the web application, defaulting to 8000 and 3000, respectively.

### Startup
```sh
./scripts/startup.sh
```

Once started, the backend API and web application will run in Docker containers and can be accessed at [http://localhost:8000](http://localhost:8000) and [http://localhost:3000](http://localhost:3000), respectively.

### Shutdown
```sh
./scripts/shutdown.sh
```