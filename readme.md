# HeadHunter Vacancy Fetcher

This Python script allows you to fetch and store job vacancies data from HeadHunter API for specified companies.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- PostgreSQL

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/gvriil/CW5.git
    cd your-repo
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

3. Set up your PostgreSQL database. Create a `database.ini` file with your database configuration:

    ```ini
    [postgresql]
    user = your_username
    password = your_password
    host = your_host
    port = your_port
    ```

4. Run the script:

    ```bash
    poetry run python main.py
    ```

## Configuration

The script uses a configuration file (`database.ini`) to connect to your PostgreSQL database. Ensure the file is correctly set up with your database details.

## Usage

1. The script fetches job vacancies for specified companies. You can customize the list of companies in the `companies.json` file.

2. Run the script using the command:

    ```bash
    poetry run python main.py
    ```

3. Follow the on-screen menu to perform various actions, such as fetching and storing vacancies, displaying company information, and more.

## Companies Configuration

The list of companies and their IDs are stored in the `companies.json` file. You can edit this file to add or remove companies.

```json
{
  "companies": [
    {"name": "Company1", "id": 123},
    {"name": "Company2", "id": 456},
    ...
  ]
}
