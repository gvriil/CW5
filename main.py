import json

from api.hh_api import HeadHunterApi
from db_manager import DBManager


def get_user_choice():
    """
       Получает ввод пользователя для выбора опции в меню.

       Возвращает:
       str: Выбранная пользователем опция.
    """
    user_choice = input("Введите номер выбранной опции: ")
    return user_choice


def print_menu():
    """
       Выводит основное меню с пронумерованными опциями.
       """
    print("Меню:")
    print("1. Получить и сохранить вакансии")
    print("2. Показать компании и количество вакансий")
    print("3. Показать все вакансии")
    print("4. Средняя з/п")
    print("5. Макс. з/п")
    print("6. Вакансии по запросу")
    print("0. Выход")


def display_companies_and_vacancies(data):
    """
       Выводит информацию о компаниях и количестве вакансий.

       Аргументы:
       data (list): Список данных о компаниях и их вакансиях.
    """
    if data:
        print("company_name | count")
        print("-" * 50)
        for row in data:
            print(f"{row[0]} | {row[1]}")
        print("-" * 50)
        print(f"Всего строк: {len(data)}")
    else:
        print("Нет данных о компаниях и вакансиях.")


def fetch_and_save_vacancies(company_ids, hh, db_manager):
    """
       Получает и сохраняет вакансии для указанных компаний.

       Аргументы:
       company_ids (list): Список идентификаторов компаний.
       hh: Экземпляр HeadHunterApi.
       db_manager: Экземпляр DBManager.
    """
    vacancy_data = []

    for id_ in company_ids:
        try:
            vacancies = hh.get_vacancies(id_['id'])
            vacancy_data.extend(vacancies)
        except Exception as e:
            print(f"Error fetching vacancies for company {id_}: {e}")

    for data in company_ids:
        print(1)
        db_manager.insert_data_company(int(data["id"]), data["name"])

    for vacancy in vacancy_data:
        print(2)
        db_manager.insert_data_vacancy(vacancy.id, vacancy.employer_id,
                                       vacancy.name, vacancy.data_published,
                                       vacancy.salary_average, vacancy.area,
                                       vacancy.url, vacancy.requirement,
                                       vacancy.experience, vacancy.employment)


def load_config(file_path='config.json'):
    """
        Загружает данные конфигурации из JSON-файла.

        Аргументы:
        file_path (str, необязательно): Путь к файлу конфигурации. По умолчанию 'config.json'.

        Возвращает:
        dict: Данные конфигурации.
        """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


if __name__ == '__main__':
    config = load_config()

    # Используйте данные из конфига
    companies = config['companies']
    db_params = config['db_params']

    # Создайте экземпляр DBManager, используя данные из конфига
    db_manager = DBManager(database_name=db_params['dbname'], params=db_params)

    hh = HeadHunterApi()

    fetch_and_save_vacancies(companies, hh, db_manager)

    while True:
        print_menu()
        user_choice = get_user_choice()

        if user_choice == "1":
            fetch_and_save_vacancies(companies, hh, db_manager)
        elif user_choice == "2":
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            display_companies_and_vacancies(companies_and_vacancies)
        elif user_choice == "3":
            all_vacancies = db_manager.get_all_vacancies()
            # реализация вывода all_vacancies
        elif user_choice == "4":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя з/п: {avg_salary[0]}")
            # реализация вывода avg_salary
        elif user_choice == "5":
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            # реализация вывода higher_salary_vacancies
        elif user_choice == "6":
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            # реализация вывода keyword_vacancies
        elif user_choice == "0":
            db_manager.close_connection()
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите корректное число.")
