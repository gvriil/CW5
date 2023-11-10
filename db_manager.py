import logging

import psycopg2


def connect_decorator(func):
    def wraper(self, *args, **kwargs):

        conn = psycopg2.connect(**self.params)
        cursor = conn.cursor()
        if len(args) > 0:
            if isinstance(args[0], (dict, list, tuple)):
                query, data = func(self, args[0])
                cursor.executemany(query, data)
            else:
                query = func(self, args[0])
                cursor.execute(query)

        else:
            query = func(self)
            cursor.execute(query)

        if func.__name__.startswith('get_'):
            collumn = [i.name for i in cursor.description]
            row = cursor.fetchall()
            print(collumn, row)

        conn.commit()
        cursor.close()
        conn.close()

    return wraper


class DBManager:
    """
    Этот класс предназначен для создания и управления базой данных
    """

    def __init__(self, database_name: str, params: dict):
        self.name = database_name
        self.params = params
        self.create_database()
        self.create_table_companies()
        self.create_table_vacancies()

    def select_query(self, query: str):
        """
        Выполняет SQL-запрос с возможными значениями
        :param query: str
        :param values: tuple
        :return: None
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchone()[0]
        except psycopg2.Error as e:
            logging.error(f"Error executing query: {e}")
        return result

    def execute_query(self, query: str, values: tuple = None):
        """
        Выполняет SQL-запрос с возможными значениями
        :param query: str
        :param values: tuple
        :return: None
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    if values:
                        cur.execute(query, values)
                    else:
                        cur.execute(query)
        except psycopg2.Error as e:
            logging.error(f"Error executing query: {e}")

    def create_database(self):
        """
        Этот метод создает базу данных "cw5", если она не существует.
        :return: None
        """
        self.params['dbname'] = 'postgres'
        # Удаляем базу данных, если она уже существует
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE IF EXISTS {self.name}")
        except psycopg2.Error as e:
            logging.error(f"Ошибка создания базы данных: {e}")
        finally:
            cur.close()
            conn.close()
        # Создаем новую базу данных
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f'CREATE DATABASE {self.name}')

            # Обновляем параметры подключения к базе данных
            self.params.update({'dbname': self.name})
        except psycopg2.Error as e:
            logging.error(f"Ошибка создания базы данных: {e}")
        finally:
            cur.close()
            conn.close()

    @connect_decorator
    def create_table_companies(self):
        """
        Метод для создания таблицы компаний
        :return: None
        """
        query = '''CREATE TABLE IF NOT EXISTS companies (
                company_id_hh integer PRIMARY KEY,
                company_name varchar(150),
                employer_url varchar(150)
            )'''
        return query

    # def create_table_companies(self):
    #     """
    #     Метод для создания таблицы компаний
    #     :return: None
    #     """
    #     query = '''CREATE TABLE companies (
    #             company_id_hh integer PRIMARY KEY,
    #             company_name varchar(150),
    #             employer_url varchar(150)
    #         )'''
    #     self.execute_query(query)
    @connect_decorator
    def create_table_vacancies(self):
        """
        Метод для создания таблицы вакансий
        :return: None
        """
        query = '''CREATE TABLE vacancies (
                vacancy_id_hh integer PRIMARY KEY,
                company_id_hh integer,
                vacancy_name varchar(150),
                data_published date,
                salary_average integer,
                area varchar(150),
                url varchar(150),
                requirement varchar(500),
                experience varchar(150),
                employment varchar(150),
                CONSTRAINT fk_hh_vacancies_vacancies FOREIGN KEY(company_id_hh) REFERENCES companies(company_id_hh)
            )'''
        return query
    # def create_table_vacancies(self):
    #     """
    #     Метод для создания таблицы вакансий
    #     :return: None
    #     """
    #     query = '''CREATE TABLE vacancies (
    #             vacancy_id_hh integer PRIMARY KEY,
    #             company_id_hh integer,
    #             vacancy_name varchar(150),
    #             data_published date,
    #             salary_average integer,
    #             area varchar(150),
    #             url varchar(150),
    #             requirement varchar(500),
    #             experience varchar(150),
    #             employment varchar(150),
    #             CONSTRAINT fk_hh_vacancies_vacancies FOREIGN KEY(company_id_hh) REFERENCES companies(company_id_hh)
    #         )'''
    #     self.execute_query(query)

    @connect_decorator
    def insert_data_company(self, data: list):
        """
        Метод для вставки данных в таблицу компаний
        :param data: Словарь с данными компании
        :return: None
        """
        query = "INSERT INTO companies VALUES (%s, %s)"
        return query, data

    # def insert_data_company(self, data: dict):
    #     """
    #     Метод для вставки данных в таблицу компаний
    #     :param data: Словарь с данными компании
    #     :return: None
    #     """
    #     query = "INSERT INTO companies VALUES (%s, %s)"
    #     values = (
    #         int(data["id"]), data["name"])
    #     # data["employer"]["alternate_url"])
    #     self.execute_query(query, values)

    @connect_decorator
    def get_companies_and_vacancies_count(self):
        """
        Получение количества компаний и вакансий в базе данных.
        """
        query = '''SELECT c.company_name, 
                COUNT(c.company_name) AS "кол-во вакансий"
FROM vacancies v
JOIN companies c USING(company_id_hh)
GROUP BY c.company_name
ORDER BY 2 DESC'''
        return query

    @connect_decorator
    #олучает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    def get_all_vacancies(self):
        query = '''
                    SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                    FROM vacancies v
                    JOIN companies c USING (company_id_hh);
                '''
        return query

    @connect_decorator
    def get_avg_salery(self):
        query = '''
                    SELECT  ROUND(AVG(salary_average),2 ) 
                    FROM vacancies;
                '''
        return query

    @connect_decorator
    def get_vacancies_with_higher_salary(self):
        query = '''
                    SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                    FROM vacancies v
                    JOIN companies c USING (company_id_hh)
                    WHERE v.salary_average > (SELECT ROUND(AVG(salary_average),2 ) FROM vacancies);
                '''
        return query


    @connect_decorator
    #получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
    def get_vacancies_with_keyword(self, word):
        query = f'''
                    SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                    FROM vacancies v
                    JOIN companies c USING (company_id_hh)
                    WHERE (v.vacancy_name) LIKE '%{word}%';                                 
                '''
        return query
    @connect_decorator
    def insert_data_vacancy(self, data: list):
        """
        Метод для вставки данных в таблицу вакансий
        :param vacancies: Список объектов вакансий
        :return: None
        """
        query = "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        return query, data

    # def insert_data_vacancy(self, vacancies: list):
    #     """
    #     Метод для вставки данных в таблицу вакансий
    #     :param vacancies: Список объектов вакансий
    #     :return: None
    #     """
    #     query = "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #     for vacancy in vacancies:
    #         values = (vacancy.id, vacancy.employer_id, vacancy.name, vacancy.data_published,
    #                   vacancy.salary_average, vacancy.area, vacancy.url, vacancy.requirement,
    #                   vacancy.experience, vacancy.employment)
    #
    #         self.execute_query(query, values)

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                conn.close()
        except psycopg2.Error as e:
            logging.error(f"Error closing connection: {e}")

# Остальные методы также могут использовать execute_query для выполнения SQL-запросов
