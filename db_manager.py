import psycopg2


class DBManager:
    def __init__(self, database_name: str, params: dict):
        """
        Инициализация объекта DBManager.

        :param database_name: Имя базы данных.
        :param params: Параметры подключения к базе данных.
        """
        self.name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получение количества вакансий у каждой компании.

        :return: Список кортежей (название компании, количество вакансий).
        """
        try:
            conn = psycopg2.connect(database=self.name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    '''
                        SELECT company_name, COUNT(*) FROM companies
                        JOIN vacancies USING (company_hh_id)
                        GROUP BY company_name 
                    '''
                )
                result = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            raise e
        finally:
            conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получение всех вакансий с указанием компании, названия, URL и зарплаты.

        :return: Список кортежей (название компании, название вакансии, URL, зарплата).
        """
        try:
            conn = psycopg2.connect(database=self.name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    '''
                        SELECT company_name, vacancy_name, url, salary
                        FROM vacancies 
                        JOIN companies USING (company_hh_id) 
                    '''
                )
                result = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            return e
        finally:
            conn.close()
        return result

    def get_avg_salary(self):
        """
        Получение средней зарплаты по всем вакансиям.

        :return: Средняя зарплата (округленная до двух знаков после запятой).
        """
        try:
            conn = psycopg2.connect(database=self.name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    '''
                        SELECT ROUND(AVG(salary), 2)
                        FROM vacancies;
                    '''
                )
                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            raise e
        finally:
            conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получение вакансий с зарплатой выше средней.

        :return: Список кортежей с информацией о вакансиях и компаниях.
        """
        try:
            conn = psycopg2.connect(database=self.name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    '''
                        SELECT * FROM vacancies v
                        JOIN companies c USING (company_hh_id)
                        WHERE v.salary > (SELECT ROUND(AVG(salary),2 ) FROM vacancies);
                    '''
                )
                result = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            raise e
        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, word):
        """
        Получение вакансий, содержащих ключевое слово в названии.

        :param word: Ключевое слово для поиска.
        :return: Список кортежей с информацией о вакансиях и компаниях.
        """
        try:
            conn = psycopg2.connect(database=self.name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    f'''
                        SELECT c.company_name, v.vacancy_name, v.salary, v.url
                        FROM vacancies v
                        JOIN companies c USING (company_hh_id)
                        WHERE LOWER(v.vacancy_name) LIKE '%{word}%';
                    '''
                )
                result = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            raise e
        finally:
            conn.close()
        return result
