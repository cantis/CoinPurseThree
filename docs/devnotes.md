# Dev Notes

**16 Sept 23**

I have uvicorn installed and it runs on windows or in the devcontainer! The command to run it is
```powershell
PS uvicorn main:app --reload
```
The site is up at http://localhost:8000/ and the docs are at http://localhost:8000/docs

*NOTE: An alternative format for the docs is http://localhost:8000/redoc*

## Devcontainer
The app also has a .devcontainer configured with it, works well starts up smoothly and runs

The container image that I have chosen also includes a postgresql server, so I can use that for the database details on this are at https://github.com/devcontainers/templates/tree/main/src/postgres

## Tasks
* [x] Add a devcontainer
* [x] Split the app into a main.py a router.py and a several routers
* [ ] Add Models for Player, Character, Transaction
* [ ] Add a database connection
* [ ] Add a database migration
* [ ] Add a database seed

## Alembic notes

To initialize alembic (creates a folder called alembic)
`PS alembic init alembic `

To create a migration
`PS alembic revision --autogenerate -m "create player table" `

To run the migration
`PS alembic upgrade head `

To create alembic database
`PS alembic upgrade head `