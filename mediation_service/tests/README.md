# Unit tests
This directory contains unit tests for mediation service

Tests can be run using pytest or `make test` target from the repository root directory.

### Note: pytest imports
Python's sys.path array defines search paths for modules.
An action has been added to conftest.py to append the path to the `mediation` module to sys.path. This action occurs before any tests are run and ensures pytest has the correct paths to import modules.

### Load Tests
A basic load test can be found within the `performance` directory, using the `Locust` library this test can be run with
`locust -f locustfile.py`. The following environment variables will need to be set prior to running locust:
- `LOCUST_HOST="https://internal-dev.api.service.nhs.uk"`
- `CALLBACK_URL="https://nhsd-apim-testing-internal-dev.herokuapp.com/callback"`
- `CLIENT_ID="<your-client-id>"`
- `CLIENT_SECRET="<your-client-secret>"`

Using Locust, set a value for the peak concurrent users, the user spawn rate, and set the host to `http://localhost:5000`
