# NOTE: DO NOT FORK THIS REPOSITORY. CLONE AND SETUP A STANDALONE REPOSITORY.

# Adbrew Test!

Hello! This test is designed to specifically test your Python, React and web development skills. The task is unconventional and has a slightly contrived setup on purpose and requires you to learn basic concepts of Docker on the fly. 


# Structure

This repository includes code for a Docker setup with 3 containers:
* App: This is the React dev server and runs on http://localhost:3000. The code for this resides in src/app directory.
* API: This is the backend container that run a Django instance on http://localhost:8000. 
* Mongo: This is a DB instance running on port 27017. Django views already have code written to connect to this instance of Mongo.

We highly recommend you go through the setup in `Dockerfile` and `docker-compose.yml`. If you are able to understand and explain the setup, that will be a huge differentiator.

# Setup
1. Clone this repository (DO NOT FORK)
```
git clone https://github.com/adbrew/test.git
```
2. Change into the cloned directory and set the environment variable for the code path. Replace `path_to_repository` appropriately.
```
export ADBREW_CODEBASE_PATH="{path_to_repository}/test/src"
```
3. Build container (you only need to build containers for the first time or if you change image definition, i.e., `Dockerfile`). This step will take a good amount of time.
```
docker-compose build
```
4. Once the build is completed, start the containers:
```
docker-compose up -d
```
5. Once complete, `docker ps` should output something like this:
```
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                      NAMES
e445be7efa61   adbrew_test_api     "bash -c 'cd /src/re…"   3 minutes ago   Up 2 seconds   0.0.0.0:8000->8000/tcp     api
0fd203f12d8a   adbrew_test_app     "bash -c 'cd /src/ap…"   4 minutes ago   Up 3 minutes   0.0.0.0:3000->3000/tcp     app
884cb9296791   adbrew_test_mongo   "/usr/bin/mongod --b…"   4 minutes ago   Up 3 minutes   0.0.0.0:27017->27017/tcp   mongo
```
6. Check that you are able to access http://localhost:3000 and http://localhost:8000/todos
7. If the containers in #5 or #6 are not up, we would like you to use your debugging skills to figure out the issue. Only reach out to us if you've exhausted all possible options. The `app` container may take a good amount of time to start since it will download all package dependencies.

# Tips
1. Once containers are up and running, you can view container logs by executing `docker logs -f --tail=100 {container_name}` Replace `container_name` with `app` or `api`(output of `docker ps`)
2. You can enter the container and inspect it by executing `docker exec -it {container_name} bash` Replace `{container_name}` with `app` or `api` (output of `docker ps`)
3. Shut all containers using `docker-compose down`
4. Restart a container using `docker restart {container_name}`


# Task

When you run `localhost:3000`, you would see 2 things:
1. A form with a TODO description textbox and a submit button. On this form submission, the app should interact with the Django backend (`POST http://localhost:8000/todos`) and create a TODO in MongoDB.
2. A list with hardcoded TODOs. This should be changed to reflect TODOs in the backend (`GET http://localhost:8000/todos`). 
3. When the form is submitted, the TODO list should refresh again and fetch latest list of TODOs from MongoDB.

# Instructions [IMPORTANT] 
1. All React code should be implemented using [React hooks](https://reactjs.org/docs/hooks-intro.html) and should not use traditional stateful React components and component lifecycle method.
2. Do not use Django's model, serializers or SQLite DB. Persist and retrieve all data from the mongo instance. A `db` instance is already present in `views.py`.
3. Do not bypass the Docker setup. Submissions that do not have proper docker setup will be rejected.
4. We are looking for developers who have strong fundamentals and can ramp up fast. We expect you to learn and grasp basic React Hooks/Mongo/Docker concepts on the fly.
5. Do not fork this repository or submit your solution as a PR since this is a public repo and there are other candidates taking the same test. Send us a link to your repo privately.
6. If you are able to complete the test, we will have a live walkthrough of your code and ask questions to check your understanding.
7. The code for the actual solution is pretty easy. The code quality in your solution should be production-ready - error handling, abstractions, well-maintainable and modular code. If you're not aware, we recommend reading a bit about software design principles and applying them (both JS and Python). Here are some reading resources to get you started:
   * https://kinsta.com/blog/python-object-oriented-programming/
   * https://realpython.com/solid-principles-python/
   * https://www.toptal.com/python/python-design-patterns

---

# Solution Implementation

## Architecture Overview

This implementation follows **production-grade architecture** with SOLID principles and clean code practices.

### Backend Architecture (Django + MongoDB)

```
src/rest/rest/
├── core/
│   ├── database.py      # MongoDBConnection (Singleton Pattern)
│   └── logger.py        # AppLogger (Singleton Pattern)
├── exceptions/
│   └── base.py          # Custom exceptions hierarchy
├── validators/
│   └── todo.py          # TodoValidator (input validation)
├── serializers/
│   └── todo.py          # TodoSerializer (data transformation)
├── repositories/
│   └── todo.py          # TodoRepository (data access layer)
├── services/
│   └── todo.py          # TodoService (business logic)
├── tests/               # Pytest test suite (39 tests)
│   ├── conftest.py
│   ├── test_validators.py
│   ├── test_serializers.py
│   ├── test_repositories.py
│   └── test_views.py
├── views.py             # API endpoints
└── urls.py              # URL routing
```

**Design Patterns Used:**
- **Singleton Pattern**: Database connection, Logger
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic separation
- **Custom Exception Hierarchy**: Centralized error handling

### Frontend Architecture (React + Hooks)

```
src/app/src/
├── api/
│   └── TodoAPI.js       # API client with error handling
├── hooks/
│   └── useTodos.js      # Custom hook for state management
├── components/
│   ├── TodoForm.js      # Form component
│   ├── TodoList.js      # List + Item components
│   ├── ErrorMessage.js  # Error display + logging
│   ├── ConfirmDialog.js # Modal confirmation
│   └── ClearAllButton.js# Clear all with confirmation
├── __tests__/           # Jest test suite (31 tests)
│   ├── TodoAPI.test.js
│   ├── useTodos.test.js
│   ├── TodoForm.test.js
│   ├── TodoList.test.js
│   └── App.test.js
├── App.js               # Main component
└── App.css              # Professional styling
```

**Design Patterns Used:**
- **Custom Hooks**: State management abstraction
- **Component Composition**: Modular UI components
- **Error Boundary Pattern**: Graceful error handling
- **Separation of Concerns**: API, hooks, components

## Features

- ✅ Create TODO items
- ✅ List all TODOs (latest first)
- ✅ Delete individual TODO
- ✅ Clear all TODOs (with confirmation)
- ✅ Form validation
- ✅ Error handling with user-friendly messages
- ✅ Loading states
- ✅ Professional UI styling

## Running Tests

### Backend Tests (39 tests)
```bash
# Run inside Docker container
docker-compose exec api pytest -v

# With coverage
docker-compose exec api pytest -v --cov=rest --cov-report=term-missing
```

### Frontend Tests (31 tests)
```bash
# Run locally
cd src/app
npm test -- --watchAll=false

# With coverage
npm test -- --watchAll=false --coverage
```

## CI/CD Pipeline

The project includes a GitHub Actions CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:

1. **On every push/PR:**
   - Runs backend tests (pytest with MongoDB service)
   - Runs frontend tests (Jest)
   - Uploads coverage reports

2. **On push to main:**
   - Builds Docker images
   - Pushes to Docker Hub
   - Deploys to AWS EC2

3. **On PRs:**
   - Runs code quality checks (flake8, black, ESLint)

### Required GitHub Secrets

```
DOCKER_USERNAME      # Docker Hub username
DOCKER_PASSWORD      # Docker Hub password
AWS_ACCESS_KEY_ID    # AWS credentials
AWS_SECRET_ACCESS_KEY
EC2_HOST             # EC2 instance public IP
EC2_USERNAME         # EC2 SSH username (e.g., ubuntu)
EC2_SSH_KEY          # EC2 SSH private key
```

### Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
DOCKER_USERNAME=your-username TAG=latest docker-compose -f docker-compose.prod.yml up -d
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos/` | List all TODOs |
| POST | `/api/todos/` | Create a TODO |
| DELETE | `/api/todos/<id>/` | Delete a TODO |
| DELETE | `/api/todos/clear/` | Delete all TODOs |
