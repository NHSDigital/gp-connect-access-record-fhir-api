# Unit tests
This directory contains unit tests for mediation service

Tests can be run using pytest or `make test` target from the repository root directory.

### Note: pytest imports
Python's sys.path array defines search paths for modules.
An action has been added to conftest.py to append the path to the `mediation` module to sys.path. This action occurs before any tests are run and ensures pytest has the correct paths to import modules.