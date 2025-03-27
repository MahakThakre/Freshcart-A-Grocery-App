# Project Setup Guide

## Prerequisites

Make sure you have the following tools installed:

- [WSL (Windows Subsystem for Linux)](https://docs.microsoft.com/en-us/windows/wsl/)

## Installation Steps

1. Open a WSL terminal:

    ```bash
    wsl
    ```

2. Navigate to the Backend directory and activate the virtual environment:

    ```bash
    cd Backend
    source venv/bin/activate
    ```

3. Install Python dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

Now, open 6 terminals with wsl:

### Terminal 1: Frontend

Navigate to the frontend directory and run the development server:

    ```bash
    cd frontend
    npm run serve
    ```

### Terminal 2: Backend

Navigate to the Backend directory: 

    ```bash
    cd Backend
    ```

Activate the virtual environment: 

    ```bash
    source venv/bin/activate
    ```
    
Start the backend server: 

    ```bash
    python app.py
    ```

### Terminal 3:

Activate the virtual environment: 

    ```bash
    source venv/bin/activate
    ```
 
Start the Redis server: 

    ```bash
    redis-server
  ```
 To stop redis server:

    redis-server
    sudo service redis-server stop

    sudo lsof -i :6379
    sudo kill -9 PID

### Terminal 4:

Activate the virtual environment: 

    ```bash 
    source venv/bin/activate
    ```

Start the Celery worker: 

    ```bash
    celery -A app.celery worker -l info
    ```

#### Terminal 5:

Activate the virtual environment: 

    ```bash
    source venv/bin/activate
    ```

Start the Celery beat:

    ```bash
     celery -A app.celery beat --max-interval 2 -l info
    ```

### Terminal 6:

Outside of virtual environment, run the MailHog server:

    ```bash
     ~/go/bin/MailHog
     ```
