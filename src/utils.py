from typing import Any
import requests
import psycopg2


def get_employers_id(employers: list[str]) -> list:
    """Получение списка id работодателей"""

    headers = {'User-Agent': 'HH-User-Agent'}
    params = {'text': '', 'sort_by': 'by_vacancies_open'}
    url = 'https://api.hh.ru/employers'

    employers_id = []
    for employer in employers:
        params['text'] = employer
        response = requests.get(url, params, headers=headers)
        search_result = response.json().get('items', [])
        if search_result:
            employers_id.append(search_result[0].get('id', ''))

    return employers_id


def get_employers_data(employers_id: list) -> list[dict]:
    """Получение данных о работодателях"""

    headers = {'User-Agent': 'HH-User-Agent'}

    employers_data = []
    for emp_id in employers_id:
        employer_id = emp_id
        url = f'https://api.hh.ru/employers/{employer_id}'
        response = requests.get(url, headers=headers)
        search_result = response.json()
        employers_data.append(search_result)

    return employers_data


def get_vacancies_data_by_employer(employers_id) -> list[dict]:
    """Получение данных о вакансиях конкретного работодателя"""

    headers = {'User-Agent': 'HH-User-Agent'}
    params = {'employer_id': '', 'page': 0, 'per_page': 100}
    url = 'https://api.hh.ru/vacancies'

    vacancies_by_employer = []

    for id_emp in employers_id:
        params['employer_id'] = id_emp
        params['page'] = 0
        vacancies_to_add = []
        pages_limit = requests.get(url, params, headers=headers).json().get("pages")

        while params.get('page') != pages_limit:
            response = requests.get(url, params, headers=headers)
            vacancies = response.json().get('items', [])
            vacancies_to_add.extend(vacancies)
            params['page'] += 1

        vacancies_by_employer.append({id_emp: vacancies_to_add})

    return vacancies_by_employer


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'DROP DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        pass

    cur.execute(f'CREATE DATABASE {database_name}')
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                industries TEXT,
                country VARCHAR(50),
                open_vacancies INTEGER,
                alternate_url TEXT,
                site_url TEXT
                )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR NOT NULL,
                requirement TEXT,
                responsibility TEXT,
                salary_min INT,
                salary_max INT,
                alternate_url TEXT
                )
        """)

    conn.commit()
    conn.close()
