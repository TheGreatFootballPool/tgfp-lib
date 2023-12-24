# tgfp-lib

Instructions for testing / using tgfp lib

To run tests:
* Run the 'run' configuration for 'Run Tests'

## Instructions below are for setting up the test DB

1. [DB] Create the dev `stack.env` file
   - `create_dev_env.sh`
2. [DB] Get the IP address of your dev machine (we'll call it `<dev_ip_address>` below)
   - `ipconfig getifaddr en0`
3. [DB] Get the production mongo DB password from 1Password `<prod_db_pass>`
   - `python prefect_fetch.py mongo-root-password-production`

### Start and Initialize the database

1. [DB] Use the [dev docker compose](dev-docker-compose.yaml) file for development
2. [DB] Start the mongo-db service from `dev-docker-compose`
3. [DB] Connect to the terminal of the container
4. [DB] Clone the Prod db for development
   1. `mongodump --username tgfp --password <prod_db_pass> --host="goshdarnedserver.lan:27017"`
   2. `rm -rf dump/admin`
   3. `mongorestore --username tgfp --password development dump/ --authenticationDatabase=admin --drop`
5. [DB] Confirm the DB looks good by checking with mongo compass gui

## Run the tests

### To publish package and update the production instance
* Run the shell script `bump_version_and_publish.sh`
* Update the following projects (in order) (instructions in each of their README's for updating)
  * `tgfp-job-runner`: https://github.com/johnsturgeon/tgfp-job-runner
  * `tgfp-web`: https://github.com/johnsturgeon/tgfp-web
