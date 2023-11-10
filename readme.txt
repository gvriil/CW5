# Project Title

## Database Project - HH.ru Data Extraction and PostgreSQL Integration

This project involves obtaining data about companies and job vacancies from the hh.ru website. The gathered information is then stored in a PostgreSQL database. The process includes using the hh.ru public API, designing database tables, and loading the acquired data into the created tables.

## Main Steps of the Project

1. **Data Extraction from hh.ru:**
   - Utilize the hh.ru public API and the `requests` library to collect data on employers and their job vacancies.
   - Choose a minimum of 10 companies that interest you for obtaining job vacancy data via the API.

2. **Database Table Design:**
   - Design PostgreSQL database tables to store the acquired data about employers and job vacancies.
   - Use the `psycopg2` library for working with the PostgreSQL database.

3. **Data Loading into Tables:**
   - Implement code to populate the PostgreSQL tables with data about employers and job vacancies.

4. **DBManager Class:**
   - Create a `DBManager` class for managing data in the database.
   - The class should connect to the PostgreSQL database and include the following methods:

     - `get_companies_and_vacancies_count()`: Retrieve a list of all companies and the count of vacancies for each company.
     - `get_all_vacancies()`: Retrieve a list of all job vacancies with details such as company name, vacancy name, salary, and vacancy URL.
     - `get_avg_salary()`: Obtain the average salary across all vacancies.
     - `get_vacancies_with_higher_salary()`: Retrieve a list of job vacancies with salaries higher than the average.
     - `get_vacancies_with_keyword(keyword)`: Retrieve a list of job vacancies containing specified keywords in their names (e.g., python).

   - Utilize the `psycopg2` library for database interaction in the `DBManager` class.

## Project Structure

- `main.py`: Python module for executing the project tasks.
- `DBManager.py`: Class definition for the `DBManager`.
- `requirements.txt`: List of project dependencies.
- `README.md`: Project documentation.

## How to Run the Project

1. Clone the project repository:

   ```bash
   git clone https://github.com/your-username/your-project.git

    Install dependencies:

    bash

pip install -r requirements.txt

Execute the main script:

bash

    python main.py

Additional Notes

    Ensure you have a PostgreSQL database server running with the necessary credentials.
    Customize the DBManager class methods based on your specific data model and requirements.

Feel free to explore and modify the project according to your needs. Happy coding!

vbnet


Replace placeholders like `your-username` and `your-project` with your actual GitHub username and project repository name. Also, adjust the project structure and instructions based on your specific implementation.
