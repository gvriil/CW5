Vacancy Data Management

This Python script manages vacancy data by interacting with the HeadHunter API and storing the information in a PostgreSQL database. It provides a simple command-line interface for users to perform various actions related to fetching, storing, and retrieving vacancy data.
Features

    Fetch and Save Vacancies: Get and save vacancy data for specified companies from the HeadHunter API.

    Display Companies and Vacancies: View a list of companies along with the count of vacancies they have.

    Execute Functions: Execute specific functions to retrieve and display different aspects of the stored data.

Usage

    Install the required dependencies:

    bash

pip install -r requirements.txt

Create a configuration file named config.json with the following structure:

json

{
  "companies": [
    {"name": "Company1", "id": 123},
    {"name": "Company2", "id": 456},
    ...
  ],
  "db_params": {
    "dbname": "your_database_name",
    "user": "your_database_user",
    "password": "your_database_password",
    "host": "your_database_host",
    "port": "your_database_port"
  }
}

Run the main script:

bash

    python main.py

    Follow the on-screen menu to interact with the script.

Functions

    Get All Vacancies: Display a list of all vacancies stored in the database.

    Get Average Salary: Show the average salary across all vacancies.

    Get Vacancies with Higher Salary: Display vacancies with a salary higher than the overall average.

    Get Vacancies with Keyword: Search for vacancies with a specific keyword in their names.

Exit

Enter 0 to exit the script. This will close the database connection and terminate the program.