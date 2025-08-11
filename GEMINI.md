# Project Overview

This project is a Python-based package tracking application built with the Flask web framework. It provides a RESTful API for managing and retrieving information about shipping packages. The application appears to have two distinct modes of operation:

1.  **Local JSON Database:** The `app.py` file implements the API using a local `packages.json` file as a data store. This is likely used for local development and testing.
2.  **Google Cloud SQL Backend:** The `main.py` file, in conjunction with `connect_connector.py`, provides a more robust implementation that connects to a Google Cloud SQL database using the Cloud SQL Python Connector and the SQLAlchemy ORM.

The API is formally defined in the `shipping.yaml` OpenAPI specification. The data model for packages is defined in `data_model.py`.

# Building and Running

## Dependencies

To run the project, you first need to install the required Python packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development (JSON Backend)

To run the application using the local `packages.json` file, execute the following command:

```bash
flask run --app app
```

This will start a local development server. The API will be available at `http://1227.0.0.1:5000`.

### Google Cloud SQL Backend

To run the application with the Google Cloud SQL backend, you need to set up the following environment variables, as defined in `vars.sh` and used in `connect_connector.py`:

```bash
export INSTANCE_CONNECTION_NAME="<your-project:your-region:your-instance>"
export DB_USER="<your-database-user>"
export DB_PASS="<your-database-password>"
export DB_NAME="<your-database-name>"
```

Once the environment variables are set, you can run the application with the following command:

```bash
flask run --app main
```

# Development Conventions

*   **API Definition:** The API is defined using the OpenAPI 3.0 specification in the `shipping.yaml` file. Any changes to the API should be reflected in this file.
*   **Database:** The application uses SQLAlchemy as an ORM for database interaction. The data models are defined in `data_model.py`.
*   **Testing:** A `tmp/tests` directory exists, suggesting that tests are written using a framework like `pytest`.
*   **Environment Variables:** For the Cloud SQL integration, environment variables are used to store database connection details. The `vars.sh` file provides a template for these variables.

# Code Reviews

When a code review is requested, you should follow the sytleguide in `.gemini/styleguide.md`.