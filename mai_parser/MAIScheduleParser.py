from bs4 import BeautifulSoup as bs4
import requests

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

def main():
    for d in get_data(base_url + group):
        print(d)

if __name__== "__main__":
  main()

