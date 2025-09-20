# WebTemplate - Django Backend

This directory contains a comprehensive Django backend template designed to serve as a robust foundation for modern web and mobile applications.

## Features

- **REST API:** A flexible and powerful REST API built with the Django Rest Framework.
- **Authentication:** A complete user management system, including registration, login, and session management, handled by the `users` app.
- **Real-time Communication:** WebSocket support is integrated using Django Channels, allowing for real-time features like live notifications and chat.
- **Background Tasks:** Asynchronous task processing is set up with Celery, ideal for handling long-running processes, sending emails, or performing other tasks without blocking the main application thread.
- **Push Notifications:** The backend is configured to send push notifications to mobile devices using Firebase Cloud Messaging (FCM).
- **Containerization:** The project includes `Dockerfile` and `docker-compose.yml` for easy setup, development, and deployment using Docker containers.

## Directory Structure

- `WebTemplate/`: The main Django project directory containing settings, URL configurations, and ASGI/WSGI entry points.
- `main_app/`: A core Django app for the primary business logic of your application.
- `users/`: A dedicated app for user authentication, profiles, and management.
- `swift/`: An app designed to provide a specific API for the Swift mobile application.
- `static/`: Contains static assets like CSS, JavaScript, and images.
- `templates/`: Holds the Django templates for rendering HTML.
- `Dockerfile`: Defines the Docker image for the Django application.
- `docker-compose.yml`: Orchestrates the deployment of the Django application, a database, and other services.

## Getting Started

There are two primary ways to get the application up and running:

### With Docker (Recommended)

1.  **Environment Variables:** Create a `.env` file in this directory to store your environment variables. You can use the following as a template:

    ```
    DJANGO_KEY=your-secret-key
    DB_NAME=your-db-name
    DB_USER=your-db-user
    DB_PASSWORD=your-db-password
    DB_HOST=db
    DB_PORT=5432
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    EMAIL_HOST_USER=your-email
    EMAIL_HOST_PASSWORD=your-email-password
    DEFAULT_FROM_EMAIL=your-default-email
    FCM_SERVER_KEY=your-fcm-server-key
    ```

2.  **Build and Run:** Use Docker Compose to build the images and start the containers:

    ```bash
    docker-compose up --build
    ```

    The application will be available at `http://localhost:8000`.

### Local Development

1.  **Virtual Environment:** Create and activate a Python virtual environment.

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Database:** Set up a local PostgreSQL database or configure the `settings.py` file to use SQLite.

4.  **Environment Variables:** Set the required environment variables in your shell.

5.  **Database Migrations:** Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

6.  **Run Server:** Start the Django development server:

    ```bash
    python manage.py runserver
    ```

## Configuration

The application is configured through environment variables, which are loaded in `WebTemplate/settings.py`. This allows for easy configuration for different environments (development, staging, production) without modifying the code.

Refer to the `settings.py` file for a complete list of configurable options.

## API Endpoints

The REST API endpoints are defined in the `urls.py` files within the `main_app`, `users`, and `swift` apps. When the application is running, you can explore the API using the browsable API provided by the Django Rest Framework.
