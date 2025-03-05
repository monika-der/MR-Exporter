# MR Exporter

MR Exporter is a Python script that fetches merge requests from GitLab from the last 30 days and posts them to a Google Sheet using Sheety.

## Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- A Sheety account (https://sheety.co/)
- A Google Sheet with a tab named in the format `MM.YYYY` (e.g., `11.2023`) and headers: `giturl`, `date`, `title`
- Refresh the project in Sheety after creating the tab

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd mr-exporter
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Create a `.env` file in the root directory and add the following environment variables:
    ```dotenv
    SHEETY_BASE_URL=https://api.sheety.co/your-sheety-base-url/
    GITLAB_BASE_URL=https://git.prisjakt.io/api/v4/merge_requests
    GITLAB_PRIVATE_TOKEN=your-gitlab-private-token
    SHEETY_BEARER_TOKEN=your-sheety-bearer-token
    AUTHOR_USERNAME=your-gitlab-username
    ```

## Usage

1. Activate the virtual environment:
    ```sh
    poetry shell
    ```

2. Run the script:
    ```sh
    python src/main.py
    ```

## Configuration

- **SHEETY_BASE_URL**: The base URL for the Sheety API.
- **GITLAB_BASE_URL**: The base URL for the GitLab API.
- **GITLAB_PRIVATE_TOKEN**: Your private token for GitLab API authentication.
- **SHEETY_BEARER_TOKEN**: Your bearer token for Sheety API authentication.
- **AUTHOR_USERNAME**: The GitLab username for which to fetch merge requests.
