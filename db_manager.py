import logging

import psycopg2


def connect_decorator(func):
    def wrapper(self, *args, **kwargs):

        conn = psycopg2.connect(**self.params)
        cursor = conn.cursor()
        try:
            if len(args) > 0:
                if isinstance(args, (dict, list, tuple)):
                    query, data = func(self, args)
                    cursor.execute(query, data)
                else:
                    query, data = func(self, args)
                    cursor.execute(query)

            else:
                query = func(self)
                cursor.execute(query)

            if func.__name__.startswith('get_'):
                column_names = [i.name for i in cursor.description]
                rows = cursor.fetchall()

                # Выводим заголовки столбцов
                print(" | ".join(column_names))
                print("-" * 50)

                # Выводим данные
                for row in rows:
                    print(row)  # Add this line to see the content of the row
                    print(f"{row[0]} | {row[1]}")  # Предполагаем, что данные о компании и количестве вакансий в первых двух столбцах

                print("-" * 50)
                print(f"Всего строк: {len(rows)}")
            # if func.__name__.startswith('get_'):
            #     column = [i.name for i in cursor.description]
            #     rows = cursor.fetchall()
            #     print(**f'вакансий в компаниях:{rows}')
        except psycopg2.Error as e:
            logging.error(f'Error executing query: {e}')
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    return wrapper


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

    def run_query(self, query: str, values: tuple = None, execute: bool = True):
        """
        Выполняет SQL-запрос с возможными значениями
        :param query: str
        :param values: tuple
        :param execute: bool, указывает, нужно ли выполнять запрос (True) или только выбирать данные (False)
        :return: None
        """
        try:
            if not query.strip():  # Check if the query is empty or contains only whitespace
                logging.warning("Trying to execute an empty query.")
                return

            with psycopg2.connect(**self.params) as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    if execute:
                        if values:
                            cur.execute(query, values)
                        else:
                            cur.execute(query)
                    else:
                        cur.execute(query)
                        result = cur.fetchone()[0]
                        return result
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
            # conn.set_session(autocommit=True)
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
        # table_exists_query = "SELECT to_regclass('companies') IS NOT NULL;"
        # if not self.run_query(table_exists_query, execute=False):
        query = '''CREATE TABLE companies (
                company_id_hh integer PRIMARY KEY,
                company_name varchar(150),
                employer_url varchar(150)
            )'''
        return query

    @connect_decorator
    def create_table_vacancies(self):
        """
        Метод для создания таблицы вакансий
        :return: None
        """
        # table_exists_query = "SELECT to_regclass('vacancies') IS NOT NULL;"
        # if not self.run_query(table_exists_query, execute=False):
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

    #

    @connect_decorator
    def insert_data_company(self, data: tuple):
        """
        Метод для вставки данных в таблицу компаний
        :param data: Словарь с данными компании
        :return: None
        """
        query = "INSERT INTO companies VALUES (%s, %s);"
        return query, data

    @connect_decorator
    def get_companies_and_vacancies_count(self):
        """
        This method for getting companies with count of vacancies
        :return: str
        """
        # query_check_data = '''SELECT COUNT(*) FROM companies;'''
        # try:
        #     with psycopg2.connect(**self.params) as conn:
        #         with conn.cursor() as cur:
        #             cur.execute(query_check_data)
        #             count = cur.fetchone()[0]
        #             if count == 0:
        #                 print("Нет данных о компаниях и вакансиях.")
        #                 return None
        # except psycopg2.Error as e:
        #     logging.error(f"Error checking data: {e}")
        #     print(f"Error checking data: {e}")

        query = '''SELECT company_name, COUNT(*)
                   FROM vacancies
                   JOIN companies USING (company_id_hh)
                   GROUP BY company_name'''
        return query

    @connect_decorator
    def get_avg_salary(self):
        query = '''
                    SELECT ROUND(AVG(salary_average), 2)
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
    # получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
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
        :param data: Список объектов вакансий
        :return: None
        """
        # company_id = data[1]  # Assuming company_id is at index 1 in the data list
        # # Check if the company_id exists in the companies table
        # if self.run_query("SELECT COUNT(*) FROM companies WHERE company_id_hh = %s", (company_id,),
        #                   execute=False) == 0:
        #     logging.error(
        #         f"Error inserting data into vacancies: Company with ID {company_id} does not exist.")
        #     return

        query = "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        return query, data

    @connect_decorator
    def get_all_vacancies(self):
        query = '''
                        SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                        FROM vacancies v
                        JOIN companies c USING (company_id_hh);
                    '''
        return query

    @connect_decorator
    def get_avg_salary(self):
        query = '''
                        SELECT ROUND(AVG(salary_average), 2)
                        FROM vacancies;
                    '''
        return query

    @connect_decorator
    def get_vacancies_with_higher_salary(self):
        query = '''
                        SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                        FROM vacancies v
                        JOIN companies c USING (company_id_hh)
                        WHERE v.salary_average > (SELECT ROUND(AVG(salary_average), 2) FROM vacancies);
                    '''
        return query

    @connect_decorator
    def get_vacancies_with_keyword(self, word):
        query = f'''
                        SELECT c.company_name, v.vacancy_name, v.salary_average, v.url
                        FROM vacancies v
                        JOIN companies c USING (company_id_hh)
                        WHERE (v.vacancy_name) LIKE '%{word}%';
                    '''
        return query

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
