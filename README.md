# NodeMCU Local Server 

An overview of the server's functionality, setup instructions, and details about its API endpoints.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Setup Instructions](#setup-instructions)
3. [API Endpoints](#api-endpoints)
   - [GET /templogs](#get-templogs)
   - [GET /templogs/week](#get-templogs-week)
   - [GET /templogs/day](#get-templogs-day)
   - [GET /templogs/hour](#get-templogs-hour)
4. [Error Handling](#error-handling)
5. [License](#license)

---

## Introduction

This server is built using Node.js and provides a RESTful API for [brief description of functionality]. 

---

## Setup Instructions

To get started with this server:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git


## API Endpoints

Below is a list of the available API endpoints for this server, including descriptions, request/response formats, and examples.

---

### GET /templogs

- **Description**: Retrieves a list of all temperature logs.
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 2346,
        "name": "sensor_1",
        "temperature": -27.81,
        "created_at": "2024-10-23T11:47:45.128Z"
      },
      {
        "id": 2345,
        "name": "sensor_0",
        "temperature": 7.69,
        "created_at": "2024-10-23T11:47:44.910Z"
      }
    ]
    ```
- **Example**:
  ```bash
  curl http://192.168.100.30:3000/templogs


### GET /templogs/week

- **Description**: Retrieves a list of all temperature logs from the past seven days in desc order by date.
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 2346,
        "name": "sensor_1",
        "temperature": -27.81,
        "created_at": "2024-10-23T11:47:45.128Z"
      },
      {
        "id": 2345,
        "name": "sensor_0",
        "temperature": 7.69,
        "created_at": "2024-10-23T11:47:44.910Z"
      }
    ]
    ```
- **Example**:
  ```bash
  curl http://192.168.100.30:3000/templogs/week


### GET /templogs/week

- **Description**: Retrieves a list of all temperature logs from the past day in desc order by date.
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 2346,
        "name": "sensor_1",
        "temperature": -27.81,
        "created_at": "2024-10-23T11:47:45.128Z"
      },
      {
        "id": 2345,
        "name": "sensor_0",
        "temperature": 7.69,
        "created_at": "2024-10-23T11:47:44.910Z"
      }
    ]
    ```
- **Example**:
  ```bash
  curl http://192.168.100.30:3000/templogs/day


### GET /templogs/hour

- **Description**: Retrieves a list of all temperature logs from the past hour in desc order by date.
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 2346,
        "name": "sensor_1",
        "temperature": -27.81,
        "created_at": "2024-10-23T11:47:45.128Z"
      },
      {
        "id": 2345,
        "name": "sensor_0",
        "temperature": 7.69,
        "created_at": "2024-10-23T11:47:44.910Z"
      }
    ]
    ```
- **Example**:
  ```bash
  curl http://192.168.100.30:3000/templogs/hour

