# Dockerized Multi-Container Application Setup

This guide explains how to set up a multi-container application with Docker, including MySQL, Redis, a backend application, and a frontend application. The containers communicate over a custom Docker network. The backend application fetches details from the `sample_table` in the MySQL database and exposes an endpoint at `/get_db_details`.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system

## Steps to Set Up the Environment

### 1. Create a Docker Network

Create a custom Docker bridge network for the containers to communicate:

```bash
docker network create db-net --driver bridge
```

### 2. Run a MySQL Container

Launch a MySQL container with the following environment variables:

- `MYSQL_ROOT_PASSWORD`: Root password for MySQL
- `MYSQL_DATABASE`: Name of the database to create
- `MYSQL_USER`: Username for database access
- `MYSQL_PASSWORD`: Password for the specified user

```bash
docker container run --name mysql -d \
  -e "MYSQL_ROOT_PASSWORD=Rootpass123*" \
  -e "MYSQL_DATABASE=mysqldb" \
  -e "MYSQL_USER=mysqluser" \
  -e "MYSQL_PASSWORD=mysqlpass" \
  --network db-net \
  mysql:8
```
Access the container and add your tables and data. In this example, i addded the table 'sample_table'
### 3. Run a Redis Container

Launch a Redis container on the same network:

```bash
docker run --name db-redis -d --network db-net redis
```

### 4. Run the Backend Application

Launch the backend container with the following environment variables:

- `REDIS_HOST`: Hostname of the Redis container
- `DB_HOST`: Hostname of the MySQL container
- `DB_NAME`: Name of the MySQL database
- `DB_USER`: Username for the MySQL database
- `DB_PASSWORD`: Password for the specified MySQL user
- `DB_TABLE`: Table name used by the application
- `REDIS_PORT`: Redis service port

Expose the backend application on port 5000:

```bash
docker container run --name db-app -d --rm \
  -e "REDIS_HOST=db-redis" \
  -e "DB_HOST=mysql" \
  -e "DB_NAME=mysqldb" \
  -e "DB_USER=mysqluser" \
  -e "DB_PASSWORD=mysqlpass" \
  -e "DB_TABLE=sample_table" \
  -e "REDIS_PORT=6379" \
  --network db-net \
  -p 5000:5000 \
  anittap/db-app-backend
```

The backend exposes an endpoint at `http://localhost:5000/get_db_details` to fetch details from the `sample_table`.

### 5. Run the Frontend Application

Launch the frontend container with the following environment variables:

- `API_SERVER`: Hostname of the backend container
- `API_SERVER_PORT`: Port where the backend application is exposed
- `APP_PORT`: Port where the frontend application runs

Expose the frontend application on port 80:

```bash
docker container run --name frontend -p 80:8080 \
  -e API_SERVER=db-app \
  -e API_SERVER_PORT=5000 \
  -e APP_PORT=8080 \
  --network db-net -it anittap/db-frontend-app
```

## Accessing the Application

- **Frontend**: Open your browser and navigate to `http://localhost`.
- **Backend Endpoint**: Access the endpoint at `http://localhost:5000/get_db_details` to fetch details from the database table `sample_table`.

## Cleanup

To stop and remove the containers:

```bash
docker container stop mysql db-redis db-app frontend
docker container rm mysql db-redis frontend
```

To remove the Docker network:

```bash
docker network rm db-net
```
