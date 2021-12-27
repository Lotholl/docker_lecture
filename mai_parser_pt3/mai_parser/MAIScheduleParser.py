from bs4 import BeautifulSoup as bs4
import requests, os
import psycopg2
from flask import Flask

app = Flask(__name__)
init = False

base_url = "https://mai.ru/education/schedule/detail.php?group="
group = "М3О-208М-20"

def get_data(url):
    weekly_schedule = []
    soup = bs4(requests.get(url).text,'html5lib')
    for tr in soup.find_all('div', class_='sc-table-day'):
        dow_data = {}
        dow_subjects = []
        dow_data["date"] = tr.div.select_one(".sc-day-header").find(text=True, recursive=False)
        dow_data["dow"] = tr.div.select_one(".sc-day-header").select_one(".sc-day").text
        subjects = tr.div.select_one(".sc-table-detail-container").div.find_all('div', recursive = False)
        dow_data["subjects"] = dow_subjects
        for s in subjects:
            subject = {}
            subject["time"] = s.select_one(".sc-item-time").text
            subject["type"] = s.select_one(".sc-item-type").text
            subject["location"] = s.select_one(".sc-item-location").find(text=True, recursive=False)
            subject["title"] = s.select_one(".sc-item-title").div.span.find(text=True, recursive=False)
            subject["lecturer"] = s.select_one(".sc-item-title").div.a.span.text
            dow_data["subjects"].append(subject)
        weekly_schedule.append(dow_data)
    return weekly_schedule

def get_pgtest():
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    database = os.environ['POSTGRES_DB']
    conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host="postgres",
            port=5432
        )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    res = cursor.fetchone()
    return str(res)


@app.route("/schedule")
def schedule():
    stdgrp = ""
    try:
        stdgrp = "М3О-" + os.environ['STDGRP'] + "М-20"
    except KeyError as err:
        stdgrp = "М3О-208М-20"
    
    res = ""
    for d in get_data(base_url + stdgrp):
        res += str(d)
    return res

@app.route("/pgtest")
def pgtest():
    res = get_pgtest()
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0')