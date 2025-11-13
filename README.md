# Library Data Pipeline

![Teaching](https://img.shields.io/badge/module-DE5M5-blue)
![Python Version](https://img.shields.io/badge/python-3.9--3.12-blue.svg)
![Open Issues](https://img.shields.io/github/issues/54F-A//library-pipeline)
![Open PRs](https://img.shields.io/github/issues-pr/54F-A//library-pipeline)
![Last Commit](https://img.shields.io/github/last-commit/54F-A//library-pipeline)
![CI](https://github.com/54F-A/library-pipeline/actions/workflows/ci.yml/badge.svg)

## Project Overview

The `library-pipeline` project provides utilities to streamline data processing from raw ingestion to cleaned, analytics-ready datasets. It focuses on improving data quality, consistency, and reproducibility for library-related datasets.

## Architecture

`Medallion Architecture`: The pipeline follows a **bronze → silver → gold** pattern, with notebooks and scripts to process, validate, and transform data.  

See [docs/architecture/](docs/architecture/) for details.

## Setup

## Git

```sh
### Local Development

# At a prompt copy and paste the following 2 lines:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

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
```
**library-pipeline**/
├─ data/                  # Raw and processed datasets
├─ docs/                  # Documentation and diagrams
├─ fabric/notebooks/      # Exported Fabric notebooks
├─ project/               # Pipeline scripts
├─ scripts/               # Utility scripts
├─ src/                   # Core source code
├─ tests/                 # Unit and integration tests
├─ pyproject.toml         # Project configuration
├─ requirements.txt       # Python dependencies
└─ README.md              # Project documentation
```

## Data Sources

The pipeline uses the following datasets:

- `catalogue.xlsx` – Library catalog containing book metadata and classifications.
- `circulation_data.csv` – Records of book checkouts and returns.
- `events_data.json` – Library event schedules and attendee information.
- `feedback.txt` – Raw user feedback and comments collected from library users.

## Testing

This project uses **pytest** for automated testing:

- **Unit tests**: Located in the `tests/` directory, these tests cover core pipeline functions such as data transformations and validation logic.
- **Integration tests**: Validate end-to-end workflows, ensuring that raw data is correctly processed through the pipeline.
- **Coverage**: Test coverage is measured with `pytest-cov` for all modules in `src/`. The CI workflow enforces a minimum coverage of 70%.

To run tests locally:

- pytest tests/ -v
- pytest tests/ -v --cov=src --cov-report=term-missing

## CI/CD

This project uses GitHub Actions for continuous integration.

See [.github/workflows/ci.yml](.github/workflows/ci.yml)

## Deployment to Fabric
[TODO: Document Fabric deployment process]

## Team
[TODO: Add team members]
