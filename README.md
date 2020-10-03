# system-capstone

[![Python version](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)


### Installation Instructions

1. Ensure that you have [Git](https://git-scm.com/downloads) and a version of [Docker](https://www.docker.com/get-started) installed.

2. Move to the directory where you would like to store your local copy of the code, and clone the repository.

### Testing Instructions

Any code pushed to this repository will automatically be subject to all existing test methods as well as any newly added tests. (TODO)

To run tests locally before pushing, run `make test` on macOS or Linux, or run each command under `test` in `Makefile` separately on Windows. Running `make test` first builds a production-ready docker container with updated source files. Upon build completion, unit tests are ran.

### Deployment Instructions
1. `make sql` and `make redis` to start the databases.

2. `make run` to start a shell instance. `make benchmark` to run benchmark suite.