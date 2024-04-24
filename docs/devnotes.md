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
* [x] Add Models for Player, Character, Transaction
* [x] Add a database connection
* [x] Add a database migration
* [ ] Add a database seed (required for operation, if any)
* [ ] Add a database test seed (required for testing)
* [ ] Add Tests for Player
* [ ] Add Tests for Character
* [ ] Add Tests for Transaction

## Alembic notes

To initialize alembic (creates a folder called alembic)
`PS alembic init alembic `

To create a migration
`PS alembic revision --autogenerate -m "create player table" `

To run the migration and create the database
`PS alembic upgrade head `

**28 Feb 24**
Going to try and continue with the test setup but for now it will be with an 'on disk' database.

**7 Mar 24**
Got the tests running against a on-disk database, it's not ideal, still can't create an in-memory db
and get the tables created. But, all of the test fixture setup etc. is in the conftest and it's
now ready to be used with other tests.

