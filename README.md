# tgfp-lib

Instructions for testing / using tgfp lib

To run tests:
* Run the 'run' configuration for 'Run Tests'
* TODO: I need to set the MONGO_URI_PRD and _TST in the run configurations
* TODO: I should update these instructions to fire up a Test DB

### To publish package and update the production instance
* Run the shell script `bump_version_and_publish.sh`
* Update the following projects (in order) (instructions in each of their README's for updating)
  * `tgfp-job-runner`: https://github.com/johnsturgeon/tgfp-job-runner
  * `tgfp-web`: https://github.com/johnsturgeon/tgfp-web
