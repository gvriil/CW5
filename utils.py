import psycopg2
import requests

def get_employer_info(employer_id):
    """
    Получение информации о работодателе и его вакансиях.

    :param employer_id: Список идентификаторов работодателей.
    :return: Список словарей с информацией о работодателе и его вакансиях.
    """
    result = []
    for id in employer_id:
        url = f'https://api.hh.ru/employers/{id}'
        response_employer = requests.get(url).json()
        response_vacancies = requests.get(response_employer['vacancies_url']).json()

        if 'vacancies_url' in response_employer:
            result.append({'employer': response_employer, 'vacancies': response_vacancies['items']})
        else:
            result.append({'employer': response_employer, 'vacancies': []})

    return result

def create_database(database_name: str, params: dict[str, str]) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях.

    :param database_name: Имя базы данных.
    :param params: Параметры подключения к базе данных.
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

def create_tables(name, params):
    """
    Создание таблиц в базе данных для хранения информации о компаниях и вакансиях.

    :param name: Имя базы данных.
    :param params: Параметры подключения к базе данных.
    """
    conn = psycopg2.connect(dbname=name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE companies (
                    company_hh_id serial PRIMARY KEY,
                    company_name varchar(150),
                    employer_url varchar(150)
            )
                    """)

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE vacancies (
                    vacancy_id_hh serial PRIMARY KEY,
                    company_hh_id integer,
                    vacancy_name varchar(150),
                    salary integer,
                    url varchar(150),
                    requirement varchar(500),
                    CONSTRAINT fk_hh_vacancies_vacancies
                    FOREIGN KEY(company_hh_id)
                    REFERENCES companies(company_hh_id)
            )
                    """)

    conn.commit()
    conn.close()

def salary_format(value) -> int:
    """
    Форматирование данных о зарплате.

    :param value: Словарь с данными о зарплате.
    :return: Отформатированное значение зарплаты.
    """
    if value is not None:
        if value["from"] is not None and value["to"] is not None:
            return round((value["from"] + value["to"]) / 2)
        elif value["from"] is not None or value["to"] is not None:
            return value["from"] or value["to"]

def insert_data(data, database_name: str, params: dict) -> None:
    """
    Вставка данных о компаниях и их вакансиях в базу данных.

    :param data: Список словарей с информацией о компаниях и их вакансиях.
    :param database_name: Имя базы данных.
    :param params: Параметры подключения к базе данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            cur.execute("""
                INSERT INTO companies(company_name, employer_url) 
                VALUES (%s, %s) RETURNING company_hh_id""",
                        (item["employer"].get('name'),
                         item["employer"].get('alternate_url')))

            company_id = cur.fetchone()[0]
            for element in item["vacancies"]:
                salary = salary_format(element["salary"])

                cur.execute("""
                INSERT INTO 
                vacancies(company_hh_id, vacancy_name, salary, url, requirement) 
                VALUES (%s, %s, %s, %s, %s)
                    """, (company_id, element["name"],
                          salary,
                          element["alternate_url"],
                          element["snippet"].get("responsibility")))

    conn.commit()
    conn.close()
