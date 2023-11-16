CREATE TABLE companies (
company_id_hh serial PRIMARY KEY,
company_name varchar(150),
employer_url varchar(150)
            );

CREATE TABLE vacancies (
vacancy_id_hh serial PRIMARY KEY,
company_id_hh integer,
vacancy_name varchar(150),
salary integer,
url varchar(150),
requirement varchar(500),
CONSTRAINT fk_hh_vacancies_vacancies
FOREIGN KEY(company_id_hh)
REFERENCES companies(company_id_hh)
            );
