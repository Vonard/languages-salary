from PredictSalary import predict_rub_salary
from itertools import count
import requests
import os


def superjob_vacancies(langs):
    vacancies_sj = {}
    for lang in langs:
        salaries_sj = []
        url = "https://api.superjob.ru/2.0/vacancies/"
        for page in count(0, 1):
            payload = {
                "town": 4,
                "keyword": f"Программист {lang}",
                "count": 100,
                "page": page
            }
            headers = {
                "X-Api-App-Id": os.environ['SUPERJOB_API_TOKEN']
            }
            response = requests.get(url, params=payload, headers=headers)
            objects = response.json()["objects"]
            for object in objects:
                if (object["payment_from"] or object["payment_to"]) and object["currency"] == "rub":
                    salaries_sj.append(predict_rub_salary(object["payment_from"], object["payment_to"]))
                    # print(f'{object["profession"]}, {object["town"]["title"]}, {predict_rub_salary(object["payment_from"], object["payment_to"])}')
            if not response.json()["more"]:
                break
        try:
            average_salary = int(sum(salaries_sj) / len(salaries_sj))
        except ZeroDivisionError:
            average_salary = 0
        vacancies_sj[lang] = {"vacancies_found": response.json()["total"],
                              "vacancies_processed": len(salaries_sj),
                              "average_salary": average_salary}
    return vacancies_sj


