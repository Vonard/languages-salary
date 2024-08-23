from PredictSalary import predict_rub_salary
from itertools import count
import requests


def get_superjob_vacancies(langs, token):
    moscow_code = 4
    vacancies_sj = {}
    for lang in langs:
        salaries_sj = []
        url = "https://api.superjob.ru/2.0/vacancies/"
        for page in count(0, 1):
            payload = {
                "town": moscow_code,
                "keyword": f"Программист {lang}",
                "count": 100,
                "page": page
            }
            headers = {
                "X-Api-App-Id": token
            }
            response = requests.get(url, params=payload, headers=headers)
            json_response = response.json()
            vacancies = json_response["objects"]
            for vacancie in vacancies:
                if (vacancie["payment_from"] or vacancie["payment_to"]) and vacancie["currency"] == "rub":
                    salaries_sj.append(predict_rub_salary(vacancie["payment_from"], vacancie["payment_to"]))
            if not json_response["more"]:
                break
        try:
            average_salary = int(sum(salaries_sj) / len(salaries_sj))
        except ZeroDivisionError:
            average_salary = 0
        vacancies_sj[lang] = {"vacancies_found": json_response["total"],
                              "vacancies_processed": len(salaries_sj),
                              "average_salary": average_salary}
    return vacancies_sj
