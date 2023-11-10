class Vacancy:
    """
    Класс для представления вакансии
    """

    def __init__(self, id, employer_id, name, data_published, salary_average,
                 area, url, requirement, experience, employment):
        self.id = id
        self.employer_id = employer_id
        self.name = name
        self.data_published = data_published
        self.salary_average = salary_average
        self.area = area
        self.url = url
        self.requirement = requirement
        self.experience = experience
        self.employment = employment

    def extract_salary(self, salary):
        """
        Извлечение средней зарплаты из словаря с данными о зарплате
        :param salary: dict
        :return: int
        """
        if salary and salary['currency'] == 'RUR':
            return int((salary['from'] + salary['to']) / 2)
        else:
            return None
