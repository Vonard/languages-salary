from terminaltables import AsciiTable
from HeadHunter import headhunter_vacancies
from SuperJob import superjob_vacancies
from dotenv import load_dotenv

def create_table(vacancies, table_name):
    data = []
    data.append(['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'])
    for language, vacancies_data in vacancies.items():
        data.append([language, vacancies_data['vacancies_found'], vacancies_data['vacancies_processed'], vacancies_data['average_salary']])
            
    statistics = AsciiTable(data)
    statistics.title = table_name
    return statistics.table


def main():
    load_dotenv()
    langs = ["Python", "C++", "Javascript", "Java", "Rust", "Go", "Kotlin"]
    print(create_table(headhunter_vacancies(langs),"HeadHunter Moscow"))
    print(create_table(superjob_vacancies(langs),"SuperJob Moscow"))


if __name__ == "__main__":
    main()
