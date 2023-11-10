from datetime import datetime

import requests

from api.abc_api import API
from vacancy import Vacancy


class HeadHunterApi(API):
    """
    Класс для взаимодействия с API HeadHunter для получения вакансий.
    """

    cache = {}
    per_page = 100

    def get_vacancies(self, company_id):
        """
        Получение вакансий с помощью API HeadHunter на основе параметров поиска.

        Args:
            company_id: Идентификатор компании в HeadHunter.

        Returns:
            list[Vacancy]: Список объектов Vacancy, представляющих вакансии.
        """
        url = "https://api.hh.ru/vacancies"
        pages_amount = 1
        params = {
            "per_page": self.per_page,
            "employer_id": int(company_id)
        }
        res = []

        for page in range(pages_amount):
            params['page'] = page
            response = requests.get(url, params=params)
            if response.status_code != 200:
                raise ConnectionError('Ошибка связи с API')

            result = HeadHunterApi._data_format(response.json())
            if result:
                res.extend(result)
        return res

    @staticmethod
    def _data_format(data) -> list[Vacancy]:
        """
        Форматирование необработанных данных из ответа API в список объектов Vacancy.

        Args:
            data: Необработанные данные из ответа API.

        Returns:
            list[Vacancy]: Список объектов Vacancy.
        """
        vacancies = []
        for item in data['items']:
            id = int(item['id'])
            name = item['name']
            url = item['alternate_url']
            salary = item.get("salary")
            employer_id = int(item['employer']['id'])
            data_published = \
                datetime.fromisoformat(item.get("published_at")).strftime("%Y-%m-%d,%H:%M:%S")

            if salary:
                salary_from = salary.get('from', None)
                salary_to = salary.get('to', None)

                if salary_from and salary_to:
                    salary_average = (salary_from + salary_to) / 2
                else:
                    salary_average = salary_from if salary_from else salary_to

            else:
                salary_average = 0

            requirement = item['snippet']['requirement']
            experience = item['experience']['name']
            employment = item['employment']['name']
            area = item['area']['name']
            vacancy = Vacancy(id, employer_id, name, data_published, salary_average,
                              area, url, requirement, experience, employment)

            vacancies.append(vacancy)
        return vacancies

    @classmethod
    def area_id_search(cls, city):
        """
        Проверка правильности введенного названия города и получение его ID из API.

        Args:
            city (str): Название города.

        Returns:
            int | None: ID города или None, если не найден.
        """
        url = 'https://api.hh.ru/areas'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception('HeadHunterAPI: Ошибка запроса городов, API не работает')

        response_json = response.json()

        return cls.find_area(city, response_json)

    @classmethod
    def find_area(cls, city_title: str, areas: dict) -> int | None:
        """
        Рекурсивный поиск ID города по его названию в словаре районов.

        Args:
            city_title (str): Название города для поиска.
            areas (dict): Словарь районов с определенной структурой.

        Returns:
            int | None: ID города или None, если не найден.
        """
        for area in areas:
            if area['name'] == city_title:
                return area['id']
            elif area['areas']:
                result = cls.find_area(city_title, area['areas'])
                if result:
                    return int(result)


# if __name__ == "__main__":
#     hh = HeadHunterAPI()
#     print(hh.get_vacancies('1740'))

#
#
# # from datetime import datetime
# # import requests
# #
# # from api.abc_api import API
# # from vacancy import Vacancy
#
#
# class HeadHunterAPI(API):
#     """
#     Класс для взаимодействия с API HeadHunter для получения вакансий.
#     """
#
#     cache = {}
#     per_page = 100
#
#     def get_vacancies(self, company_id):
#         """
#         Получение вакансий с помощью API HeadHunter на основе параметров поиска.
#
#         Args:
#             search_query (dict): Словарь, содержащий параметры поиска.
#
#         Returns:
#             list[Vacancy]: Список объектов Vacancy, представляющих вакансии.
#             :param company_id:
#         """
#
#         url = "https://api.hh.ru/vacancies"
#         pages_amount = 1
#         params = {
#             # "text": search_query["text"],
#             # "area": self.area_id_search(search_query["area"]),
#             "per_page": self.per_page,
#             # "salary": 20000,
#             # "no_agreement": 1,
#             "employer_id": int(company_id)
#         }
#         res = []
#
#         for page in range(pages_amount):
#             params['page'] = page
#             response = requests.get(url, params=params)
#             if response.status_code != 200:
#                 raise ConnectionError('Ошибка связи с API')
#
#             result = HeadHunterAPI._data_format(response.json())
#             if result:
#                 res.extend(result)
#         return res
#
#     @staticmethod
#     def _data_format(data) -> list[Vacancy]:
#         """
#         Форматирование необработанных данных из ответа API в список объектов Vacancy.
#
#         Args:
#             data: Необработанные данные из ответа API.
#
#         Returns:
#             list[Vacancy]: Список объектов Vacancy.
#         """
#
#         vacancies = []
#         for item in data['items']:
#             id = int(item['id'])
#             name = item['name']
#             url = item['alternate_url']
#             salary = item.get("salary")
#             employer_id = int(item['employer']['id'])
#             data_published = \
#                 datetime.fromisoformat(item.get("published_at")).strftime("%Y-%m-%d,%H:%M:%S")
#
#             if salary:
#                 salary_from = salary.get('from', None)
#                 salary_to = salary.get('to', None)
#
#                 if salary_from and salary_to:
#                     salary_average = (salary_from + salary_to) / 2
#                 else:
#                     salary_average = salary_from if salary_from else salary_to
#
#             else:
#                 salary_average = 0
#
#             requirement = item['snippet']['requirement']
#             experience = item['experience']['name']
#             employment = item['employment']['name']
#             area = item['area']['name']
#             vacancy = Vacancy(id, employer_id, name, data_published, salary_average,
#                               area, url, requirement, experience, employment)
#
#             vacancies.append(vacancy)
#
#         return vacancies
#
#     @classmethod
#     def area_id_search(cls, city):
#         """
#         Проверка правильности введенного названия города и получение его ID из API.
#
#         Args:
#             city (str): Название города.
#
#         Returns:
#             int | None: ID города или None, если не найден.
#         """
#
#         url = 'https://api.hh.ru/areas'
#         response = requests.get(url)
#
#         if response.status_code != 200:
#             raise Exception('HeadHunterAPI: Ошибка запроса городов, API не работает')
#
#         response_json = response.json()
#
#         return cls.find_area(city, response_json)
#
#     @classmethod
#     def find_area(cls, city_title: str, areas: dict) -> int | None:
#         """
#         Рекурсивный поиск ID города по его названию в словаре районов.
#
#         Args:
#             city_title (str): Название города для поиска.
#             areas (dict): Словарь районов с определенной структурой.
#
#         Returns:
#             int | None: ID города или None, если не найден.
#         """
#

#
# # if __name__ == "__main__":
# #     hh = HeadHunterAPI()
# #     print(hh.get_vacancies('577743'))
