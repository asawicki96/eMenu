# eMenu

REST API designed to manage the dish menu.

Installation:

- Install docker & docker compose.
- Clone this repo.
-
- Make sure You have 8000 port on Your localhost free.
- Make sure You have 5432 port on Your localhost free.
- Make sure You have 6379 port on Your localhost free.

- Go into eMenu directory.
- Execute command: docker-compose up

Initial data:

To load initial data execute command:  docker exec emenu_backend_1 python manage.py loaddata db.json

Initial users:

- username: admin, password: admin
- username: user, password: userpassword

Basic endpoints:
- localhost:8000/api-token-auth/ -> token obtain endpoint,
- localhost:8000/swagger/ -> documentation,
- localhost:8000/admin/ -> django admin panel,
- localhost:8000/api/cards/ -> cards resource endpoint,
- localhost:8000/api/dishes/ -> dishes resource endpoint

Authentication:
- default auth class is IsauthenticatedOrReadOnly,
- Create, Update, Delete actions are allowed with Authorization header only.
- List, Retrieve actions are allowed to everybody.

- Authentication flow:
- User has to send his credentials which is username & password to token obtain endpoint
- The response contains auth token.
- User has to send received token with each request to protected endpoints.
- Header schema: Authorization: Token xyz...

Tests:
- There is coverage package in project dependencies.
- To run test execute command from eMenu directory: docker exec emenu_backend_1 coverage run --source='.' manage.py test
- To generate coverage report execute command from eMenu directory: docker exec emenu_backend_1 coverage report
- All commands beneath will work only when containers are running


