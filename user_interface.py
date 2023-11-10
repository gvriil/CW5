# user_interface.py

def print_companies_and_vacancies(data):
    if not data:
        print("Нет данных о компаниях и вакансиях.")
        return

    max_company_len = max(len(row[0]) for row in data)
    max_count_len = max(len(str(row[1])) for row in data)

    print("Компания".ljust(max_company_len + 5), "Кол-во вакансий".rjust(max_count_len))
    print("-" * (max_company_len + max_count_len + 10))

    for row in data:
        print(f"{row[0].ljust(max_company_len + 5)}{row[1]:>{max_count_len}}")

def print_all_vacancies(data):
    if not data:
        print("Нет данных о вакансиях.")
        return

    for row in data:
        print(f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}")

def print_avg_salary(data):
    if data:
        print(f"Средняя зарплата по вакансиям: {data[0]:.2f}")
    else:
        print("Нет данных о зарплате.")

def print_higher_salary_vacancies(data):
    if not data:
        print("Нет данных о вакансиях с зарплатой выше средней.")
        return

    for row in data:
        print(f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}")

def print_keyword_vacancies(data):
    if not data:
        print("Нет данных о вакансиях с указанными ключевыми словами.")
        return

    for row in data:
        print(f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}")
