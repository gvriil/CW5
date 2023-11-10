from abc import ABC, abstractmethod

from vacancy import Vacancy


class API(ABC):

    @abstractmethod
    def get_vacancies(self, search_query)-> list[Vacancy]:
        pass

