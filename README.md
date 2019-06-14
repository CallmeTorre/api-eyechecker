# API Eyechecker

Create `.env` file with the following variables:
```
  1 DATABASE_NAME
  2 DATABASE_PASSWORD
  3 DATABASE_HOST
  4 DATABASE_USER
  5 ENV_SELECTOR
  6 FLASK_ENV
```
To start API Eyechecker for the first time it is necessary to run the following commands in the order given:

  1. Build docker image with `docker-compose build`
  2. Start API reportes with `docker-compose up`

Now you can visit [`localhost:8080/`](http://localhost:8080/) from your browser to check the status