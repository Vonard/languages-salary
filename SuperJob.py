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
            response.raise_for_status()
            vacancies_response = response.json()
            vacancies = vacancies_response["objects"]
            for vacancy in vacancies:
                if (vacancy["payment_from"] or vacancy["payment_to"]) and vacancy["currency"] == "rub":
                    salaries_sj.append(predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"]))
            if not vacancies_response["more"]:
                break
        try:
            average_salary = int(sum(salaries_sj) / len(salaries_sj))
        except ZeroDivisionError:
            average_salary = 0
        vacancies_sj[lang] = {"vacancies_found": vacancies_response["total"],
                              "vacancies_processed": len(salaries_sj),
                              "average_salary": average_salary}
    return vacancies_sj
