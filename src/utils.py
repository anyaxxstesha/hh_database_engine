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
