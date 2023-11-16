from config import config
from db_manager import DBManager
from utils import create_database, insert_data, create_tables, get_employer_info

if __name__ == '__main__':
    """
    Основной скрипт для работы с базой данных и вывода информации пользователю.
    """

    # Получите идентификаторы компаний из вашего кода
    company_ids = [1740, 84585, 577743, 2381, 3529, 1057, 115, 903111, 4167790, 16206]
    sql_file = "query.sql"
    db_name = input("Введите название бд: ")
    params = config()
    create_database(db_name, params)
    create_tables(db_name, params)
    insert_data(get_employer_info(company_ids), db_name, params)

    # Создайте экземпляр DBManager
    db_manager = DBManager(db_name, params)

    while True:
        print("*" * 50)
        print("Меню:")
        print("1. Показать компании и количество вакансий")
        print("2. Показать все вакансии")
        print("3. Средняя з/п")
        print("4. Макс. з/п")
        print("5. Вакансии по запросу")
        print("0. Выход")
        print("*" * 50)

        user_choice = input("Ведите пункт меню: ")
        # Для каждого идентификатора компании получите информацию и вставьте ее в базу данных

        match user_choice:
            case "1":
                print(db_manager.get_companies_and_vacancies_count())
                print("*" * 50)
            case "2":
                print(db_manager.get_all_vacancies())
                print("*" * 50)
            case "3":
                print(db_manager.get_avg_salary())
                print("*" * 50)
            case "4":
                print(db_manager.get_vacancies_with_higher_salary())
                print("*" * 50)
            case "5":
                word = input("")
                print(db_manager.get_vacancies_with_keyword(word))
                print("*" * 50)
            case "0":
                quit()
            case _:
                print("неверный ввод")
                print("*" * 50)

