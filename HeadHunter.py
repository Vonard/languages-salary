from PredictSalary import predict_rub_salary
from itertools import count
import requests


def get_headhunter_vacancies(langs):
    moscow_code = 1
    vacancies = {}
    for lang in langs:
        salaries = []
        url = "https://api.hh.ru/vacancies"
        for page in count(0, 1):
            payload = {"area": moscow_code,
                       "text": f"Программист {lang}",
                       "page": page,
                       "per_page": 100}
            response = requests.get(url, params=payload)
            response.raise_for_status()
            vacancies_response = response.json()
            if page >= vacancies_response["pages"] - 1:
                break
            for vacancy in vacancies_response["items"]:
                if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR":
                    salaries.append(predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"]))
        try:
            average_salary = int(sum(salaries) / len(salaries))
        except ZeroDivisionError:
            average_salary = 0
        vacancies[lang] = {"vacancies_found": vacancies_response["found"],
                            "vacancies_processed": len(salaries),
                            "average_salary": average_salary}
    return vacancies
