# Library Data Pipeline

![CI](https://github.com/54F-A/library-pipeline/actions/workflows/ci.yml/badge.svg)

## Project Overview
[TODO: Describe the library's data quality problem]

## Architecture
[TODO: Add architecture diagram]

See [docs/architecture/](docs/architecture/) for details.

## Setup

## Git

At a prompt copy and paste the following 2 lines:

```sh
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

*Replace the template text with your details.*

### Local Development
```bash
# Clone this repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Confirm the Python 3 version
python --version

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run Python tests with a coverage report
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Project Structure
[TODO: Document your folder structure]

## Data Sources
[TODO: Describe the data files]

## Testing

This project uses **pytest** for automated testing:

- **Unit tests**: Located in the `tests/` directory, these tests cover core pipeline functions such as data transformations and validation logic.
- **Integration tests**: Validate end-to-end workflows, ensuring that raw data is correctly processed through the pipeline.
- **Coverage**: Test coverage is measured with `pytest-cov` for all modules in `src/`. The CI workflow enforces a minimum coverage of 70%.

To run tests locally:

- pytest tests/ -v
- pytest tests/ -v --cov=src --cov-report=term-missing

Current coverage: [![Coverage](https://codecov.io/gh/54F-A/library-pipeline/branch/main/graph/badge.svg)](https://codecov.io/gh/54F-A/library-pipeline)

## CI/CD

This project uses GitHub Actions for continuous integration.

See [.github/workflows/ci.yml](.github/workflows/ci.yml)

## Deployment to Fabric
[TODO: Document Fabric deployment process]

## Team
[TODO: Add team members]
