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
            json_response = response.json()
            if page >= json_response["pages"] - 1:
                break
            for vacancie in json_response["items"]:
                if vacancie["salary"] and vacancie["salary"]["currency"] == "RUR":
                    salaries.append(predict_rub_salary(vacancie["salary"]["from"], vacancie["salary"]["to"]))
            vacancies[lang] = {"vacancies_found": json_response["found"],
                               "vacancies_processed": len(salaries),
                               "average_salary": int(sum(salaries) / len(salaries))}
    return vacancies
