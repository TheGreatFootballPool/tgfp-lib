# Blank README

To run tests:
1. Install, and log in to doppler
2. Create a shell configuration to run the script text
   * `doppler setup --config tst --project greatfootballpool`
3. Add the following environment to the unit test:
   * `DOPPLER_ENV=1`

### To publish package
* poetry build
* pip install twine
* twine upload file_name.whl --repository-url https://pip.server_name.com/