from PredictSalary import predict_rub_salary
from itertools import count
import requests


def headhunter_vacancies(langs):
    vacancies = {}
    for lang in langs:
        salaries = []
        url = "https://api.hh.ru/vacancies"
        for page in count(0, 1):
            payload = {"area": "1",
                    "text": f"Программист {lang}",
                    "page": page,
                    "per_page": 100}
            response = requests.get(url, params=payload)
            response.raise_for_status()
            if page >= response.json()["pages"] - 1:
                break
            for item in response.json()["items"]:
                if item["salary"] and item["salary"]["currency"] == "RUR":
                    salaries.append(predict_rub_salary(item["salary"]["from"], item["salary"]["to"]))
            vacancies[lang] = {"vacancies_found": response.json()["found"],
                               "vacancies_processed": len(salaries),
                               "average_salary": int(sum(salaries) / len(salaries))}
    return vacancies




