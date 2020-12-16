# system-capstone

[![Python version](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)


### Installation Instructions

1. Ensure that you have [Git](https://git-scm.com/downloads) and a version of [Docker](https://www.docker.com/get-started) installed.

2. Move to the directory where you would like to store your local copy of the code, and clone the repository.

### Testing Instructions

Any code pushed to this repository will automatically be subject to all existing test methods as well as any newly added tests.

To run tests locally before pushing, run `make test` on macOS or Linux, or run each command under `test` in `Makefile` separately on Windows. Running `make test` first builds a production-ready docker container with updated source files. Upon build completion, unit tests are ran.

### Instructions

Install the necessary dependencies: MySQL, C, gcc, Make, Python3, Tweepy.

1. Create a `config.json` in the src directory by making a copy of the provided template and filling in the API keys.

2. Goto `src/c_utils/` and run `make` to compile the C ZSet shared object.

3. Generate your dataset by running `data.py` or use the existing 6k data text file.

4. Run `demo.py` or `front_end.py`.
