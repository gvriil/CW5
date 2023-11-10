from api.hh_api import HeadHunterAPI
from config import DB_PARAMS
from db_manager import DBManager
from user_interface import print_companies_and_vacancies

def fetch_and_save_vacancies(company_ids, hh, db_manager):
    vacancy_data = []

    for id_ in company_ids:
        try:
            vacancies = hh.get_vacancies(id_['id'])
            vacancy_data.extend(vacancies)
        except Exception as e:
            print(f"Error fetching vacancies for company {id_}: {e}")

    db_manager.insert_data_company([(int(data["id"]), data["name"])
                                    for data in company_ids])

    db_manager.insert_data_vacancy(
        [(vacancy.id, vacancy.employer_id, vacancy.name, vacancy.data_published,
           vacancy.salary_average, vacancy.area, vacancy.url, vacancy.requirement,
           vacancy.experience, vacancy.employment)
         for vacancy in vacancy_data])


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
        hh = HeadHunterAPI()

        fetch_and_save_vacancies(company, hh, db_manager)

        companies_and_vacancies = db_manager.get_companies_and_vacancies_count()

        if companies_and_vacancies is not None:
            print_companies_and_vacancies(companies_and_vacancies)
        else:
            print("Нет данных о компаниях и вакансиях.")

    except ConnectionError as e:
        raise e


if __name__ == '__main__':
    main()
