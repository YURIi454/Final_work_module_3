from src.file_handler import xlsx_handler_to_dict
from src.reports import spending_by_category
from src.services import categories_of_best_cashback, simple_search, search_by_phone_numbers, search_by_names
from src.views import *


def demonstration():
    """Демонстрация всего функционала."""

    demonstration_date = datetime.datetime.now()
    print('\n \033[31m! ! ! Функции API запросов заглушены - возвращают 0.0 ! ! ! \033[39m\n')
    print('Общая демонстрация функций.\n')
    print(' = = = wiews.py = = =')
    print('\n * * * ', get_greeting.__doc__, ' * * *  \n', '\n', get_greeting(demonstration_date), '\n')
    print('\n * * * ', return_courses.__doc__, ' * * *  \n', '\n', return_courses(), '\n')
    print('\n * * * ', card_number.__doc__, ' * * *  \n', '\n', card_number(xlsx_handler(PATH_XLSX)), '\n')
    print('\n * * * ', top_transactions.__doc__, ' * * * \n', '\n', top_transactions(xlsx_handler(PATH_XLSX)), '\n')
    print('\n * * * ', main_page.__doc__, ' * * *  \n', '\n', main_page(demonstration_date), '\n')
    print('\n = = = reports.py = = =  \n')
    print('\n * * * ', spending_by_category.__doc__, ' * * *  \n', '\n',
          spending_by_category(xlsx_handler(PATH_XLSX), 'Переводы'), '\n')
    print(' = = = services.py = = = ')
    print('\n * * * ', categories_of_best_cashback.__doc__, ' * * * \n', '\n',
          categories_of_best_cashback(xlsx_handler_to_dict(PATH_XLSX), '2020', '05'))
    print('\n * * * ', simple_search.__doc__, ' * * * \n', '\n',
          simple_search(xlsx_handler_to_dict(PATH_XLSX), 'Ozon.ru'))
    print('\n * * * ', search_by_phone_numbers.__doc__, ' * * * \n', '\n',
          search_by_phone_numbers(xlsx_handler_to_dict(PATH_XLSX)))
    print('\n * * * ', search_by_names.__doc__, ' * * * \n', '\n',
          search_by_names(xlsx_handler_to_dict(PATH_XLSX), 'анд'))


if __name__ == '__main__':
    demonstration()
