# HeadHunter API Data Processor

This Python application enables you to efficiently retrieve and store information about employers and their job vacancies using the HeadHunter API. The acquired data is stored in a PostgreSQL database, allowing you to execute various queries on this information.
Project Structure

## Installation and Execution 

    Clone the repository:

    bash

git clone https://github.com/gvriil/CW5.git
cd CW5

Install dependencies:

bash

pip install -r requirements.txt

### Configure the database:

    Create a database.ini file with the following format, replacing placeholders with your database details:

ini

[postgresql]
user = ваше_имя_пользователя
password = ваш_пароль
host = ваш_хост
port = ваш_порт

### Create the database:

bash

python main.py

This script automatically creates the necessary database and tables to store information about vacancies and companies.

Populate the database:

In the main.py file, specify the employer IDs in the company_ids variable, then run:

bash

python main.py

The script retrieves information about companies and their vacancies from the HeadHunter API and inserts this data into the database.

Use the console interface:

bash

    python main.py

    Follow the console instructions to execute various queries on the data.

### Notes

    Database configuration file database.ini:

    The database.ini file contains connection parameters for your PostgreSQL database. Ensure it is in the same directory as your scripts.

    Security:

    Avoid storing the database.ini file with sensitive information (such as passwords) in public repositories. Ensure this file is not included in your VCS (e.g., add it to .gitignore).

    Modifying Queries:

    If you require additional queries for the data, edit the methods in the db_manager.py file.

    Changing Database Structure:

    To make changes to the database structure, edit the create_tables methods in the db_manager.py file.

