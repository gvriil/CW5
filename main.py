from api.hh_api import HeadHunterApi
from config import DB_PARAMS
from db_manager import DBManager


#
# db_manager.create_table_companies()
# db_manager.create_table_vacancies()


def fetch_and_save_vacancies(company_ids, hh, db_manager):
    vacancy_data = []

    for id_ in company_ids:
        try:
            vacancies = hh.get_vacancies(id_['id'])
            vacancy_data.extend(vacancies)
        except Exception as e:
            print(f"Error fetching vacancies for company {id_}: {e}")

    for data in company_ids:
        db_manager.insert_data_company(int(data["id"]), data["name"])

    for vacancy in vacancy_data:
        db_manager.insert_data_vacancy(vacancy.id, vacancy.employer_id,
                                       vacancy.name, vacancy.data_published,
                                       vacancy.salary_average, vacancy.area,
                                       vacancy.url, vacancy.requirement,
                                       vacancy.experience, vacancy.employment)


def main():
    try:
        db_manager = DBManager(database_name=DB_PARAMS['dbname'], params=DB_PARAMS)

        company = [
            {"name": "Яндекс", "id": 1740}, {"name": "Авито", "id": 84585}, {"name": "Росатом",
                                                                             "id": 577743},
            {"name": "Софтлайн", "id": 2381}, {"name": "СБЕР", "id": 3529}, {"name": "Kaspersky",
                                                                             "id": 1057},
            {"name": "АйТеко", "id": 115}, {"name": "Газпром автоматизация",
                                            "id": 903111},
            {"name": "Айтеко Технолоджи",
             "id": 4167790},
            {"name": "ИКС Холдинг",
             "id": 16206}
        ]
        hh = HeadHunterApi()

        fetch_and_save_vacancies(company, hh, db_manager)

        db_manager.get_companies_and_vacancies_count()

    except ConnectionError as e:
        raise e


if __name__ == '__main__':
    main()
#     # hh = HeadHunterApi()
#     # vacancies = hh.get_vacancies('1740')
#
#     # for vacancy in vacancies:
#     #     print(f"Vacancy ID: {vacancy.id}")
#     #     print(f"Employer ID: {vacancy.employer_id}")
#     #     print(f"Name: {vacancy.name}")
#     #     print(f"Published Date: {vacancy.data_published}")
#     #     print(f"Salary Average: {vacancy.salary_average}")
#     #     print(f"Area: {vacancy.area}")
#     #     print(f"URL: {vacancy.url}")
#     #     print(f"Requirement: {vacancy.requirement}")
#     #     print(f"Experience: {vacancy.experience}")
#     #     print(f"Employment: {vacancy.employment}")
#     #     print("-" * 50)
