# RESTful Web Service

This is a RESTful web service that provides an API for managing tasks and categories.

## Technology Stack

This project uses the following technologies:

- **Flask**: A web framework for Python.
- **MySQL**: A relational database used for storing application data.
- **SQLAlchemy**: An ORM for working with the database.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **Docker Compose**: A tool for defining and running multi-container Docker applications.
- **unittest**: A library for writing and running unit tests in Python.

## Table of Contents

- [Installation and Setup](#installation-and-setup)
  - [Installation](#installation)
  - [Setup](#setup)
- [Build and Run](#build-and-run)
  - [Run](#run)
- [API Endpoints](#api-endpoints)
  - [Tasks](#tasks)
  - [Categories](#categories)
- [Request Examples](#request-examples)
  - [Create a New Task](#create-a-new-task)
  - [Get List of Tasks](#get-list-of-tasks)
- [API Resources](#api-resources)
  - [Tasks](#tasks-1)
  - [Categories](#categories-1)
- [Testing](#testing)
- [Author](#author)

## Installation and Setup

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TheRomanVolkov/To-Do-List.git
    cd To-Do-List
    ```

### Setup
2. Configure the .env file based on .env.example (define database settings and other parameters)

### Build and Run

3. Start the Docker containers:

    ```bash
    docker-compose up --build
    ```
If the tests do not pass, the build will fail, and the image will not be created.

The service will be available at http://localhost:5000

## API Endpoints

### Tasks

- **GET /tasks**: Retrieve a list of all tasks with filtering and sorting options.
- **POST /tasks**: Create a new task.
- **GET /tasks/<id>**: Get task information by its identifier.
- **PUT /tasks/<id>**: Update task information by its identifier.
- **DELETE /tasks/<id>**: Delete a task by its identifier.

### Categories

- **GET /categories**: Retrieve a list of all categories.
- **GET /categories/<id>**: Get category information by its identifier.
- **POST /categories**: Create a new category.
- **DELETE /categories/<id>**: Delete a category by its identifier.

## Request Examples

### Create a New Task

```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"title\": \"New Task\", \"description\": \"Test Description\", \"categories\": [\"Category1\"]}"
```

### Get List of Tasks
```bash
curl -X GET http://localhost:5000/tasks
```

### API Resources

#### Tasks

- **Create a New Task**
  - Method: POST
  - Path: /tasks
  - Request Body:
    ```json
    {
      "title": "Task Title",
      "description": "Task Description",
      "categories": ["category1", "category2"]
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "created_at": "2023-12-04T12:00:00Z",
      "updated_at": "2023-12-04T12:00:00Z",
      "file_path": "/uploads/file.txt",
      "categories": ["category1", "category2"]
    }
    ```

- **Get Task by ID**
  - Method: GET
  - Path: /tasks/{id}
  - Response:
    ```json
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "created_at": "2023-12-04T12:00:00Z",
      "updated_at": "2023-12-04T12:00:00Z",
      "file_path": "/uploads/file.txt",
      "categories": ["category1", "category2"]
    }
    ```

- **Update Task by ID**
  - Method: PUT
  - Path: /tasks/{id}
  - Request Body (possible fields for update):
    ```json
    {
      "title": "New Task Title",
      "description": "New Task Description",
      "categories": ["new_category"]
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "created_at": "2023-12-04T12:00:00Z",
      "updated_at": "2023-12-04T12:00:00Z",
      "file_path": "/uploads/file.txt",
      "categories": ["category1", "category2"]
    }
    ```

- **Delete Task by ID**
  - Method: DELETE
  - Path: /tasks/{id}
  - Response:
    ```json
    {
      "message": "Task and associated file deleted successfully"
    }
    ```

#### Categories

- **Get List of All Categories**
  - Method: GET
  - Path: /categories
  - Response:
    ```json
    {
      "categories": [
        {"id": 1, "name": "category1"},
        {"id": 2, "name": "category2"}
      ]
    }
    ```

- **Get Category by ID**
  - Method: GET
  - Path: /categories/{id}
  - Response:
    ```json
    {
      "category": {"id": 1, "name": "category1"}
    }
    ```

- **Create a New Category**
  - Method: POST
  - Path: /categories
  - Request Body:
    ```json
    {
      "name": "New Category"
    }
    ```
  - Response:
    ```json
    {
      "message": "Category created successfully",
      "category": {"id": 3, "name": "New Category"}
    }
    ```

- **Delete Category by ID**
  - Method: DELETE
  - Path: /categories/{id}
  - Response:
    ```json
    {
      "message": "Category deleted successfully"
    }
    ```

## Testing

To run the tests, use the following command:

```bash
docker-compose run flask_todo_app python -m unittest discover
```

This will run all the tests defined in your application.

## Author

Volkov Roman