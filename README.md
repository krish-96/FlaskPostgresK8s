# FlaskPostgresK8s

This repo was created to deploy a flask app and a postgres database in the Kubernetes

The below example shows how to set up environment variables for the flask application

```text
PYTHONUNBUFFERED=1;DB_NAME=flask_psql;DB_PASS=password;DB_USER=flask_psql;DB_HOST=localhost;DB_PORT=5432
```

To set the host and port for flask app with environment variable 
```text
PYTHONUNBUFFERED=1;DB_NAME=flask_psql;DB_PASS=password;DB_USER=flask_psql;DB_HOST=localhost;DB_PORT=5432;host=0.0.0.0;port=5052;
```
