from src.dbmanager_class import DBManager
from utils import (get_employers_id, get_employers_data, get_vacancies_data_by_employer,
                   create_database, save_data_to_database)
from config import config


def main():

    employers = [
        'ПАО Яковлев',
        'Объединенная Авиастроительная Корпорация',
        'АО Туполев',
        'Кронштадт',
        'Лаборатория Касперского',
        'Тинькофф',
        'АВИТО ТЕХ: разработка',
        'DIGINETICA',
        'Автомакон',
        'Контур'
    ]

    params = config(filename="../database.ini")

    employers_id = get_employers_id(employers)
    employers_data = get_employers_data(employers_id)
    vacancies_by_employer = get_vacancies_data_by_employer(employers_id)
    create_database('hh_database', params)
    save_data_to_database(employers_data,  vacancies_by_employer, 'hh_database', params)


if __name__ == '__main__':
    main()
