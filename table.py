from terminaltables import AsciiTable
from HeadHunter import get_headhunter_vacancies
from SuperJob import get_superjob_vacancies
from dotenv import load_dotenv
import os

def create_table(vacancies, table_name):
    table = []
    table.append(['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'])
    for language, vacancies_data in vacancies.items():
        table.append([language, vacancies_data['vacancies_found'], vacancies_data['vacancies_processed'], vacancies_data['average_salary']])
            
    statistics = AsciiTable(table)
    statistics.title = table_name
    return statistics.table


def main():
    load_dotenv()
    langs = ["Python", "C++", "Javascript", "Java", "Rust", "Go", "Kotlin"]
    superjob_token = os.environ['SUPERJOB_API_TOKEN']
    print(create_table(get_headhunter_vacancies(langs),"HeadHunter Moscow"))
    print(create_table(get_superjob_vacancies(langs, superjob_token),"SuperJob Moscow"))


if __name__ == "__main__":
    main()
