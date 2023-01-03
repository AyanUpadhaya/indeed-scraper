# https://docs.google.com/spreadsheets/d/17ZXagPqNiEMrDuTvUTRTe0eJrG_8x_dzuRZXousIRGQ/edit?usp=sharing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

master_list = []
search_term = "python web developer"
location = "California"
count = 0
base_url = "https://www.indeed.com/viewjob?"


opts = Options()
opts.add_argument(
    "user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36]")
# opts.add_argument("--headless")
opts.add_argument(
    "executable_path=[C:\\Users\\ayanU\\OneDrive\\Desktop\\Labs\\python\\bs4\\driver\\chromedriver.exe]")


def make_page_request(url, opts):
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    pageSource = driver.page_source
    time.sleep(5)
    driver.quit()
    return pageSource


def parse(html, bs):
    soup = BeautifulSoup(html, 'html.parser')
    page_title = soup.title.text
    result_contents = soup.find_all('td', class_="resultContent")

    for rc in result_contents:
        title = rc.find('h2', {'class': 'jobTitle'}).text
        company_location = rc.find('div', {'class': 'company_location'}).text
        company_name = rc.find('span', {'class': 'companyName'}).text
        try:
            salary = rc.find('div', {'class': 'salaryOnly'}).text
        except Exception as e:
            salary = "NA"
        url_link = base_url + \
            rc.find('a', {'class': 'jcs-JobTitle'}).get('href').split('?')[-1]

        master_list.append({'title': title, 'company_name': company_name,
                           'company_location': company_location, 'salary': salary, 'link': url_link})


for i in range(1, 6):
    url = f"https://www.indeed.com/jobs?q={search_term}&l={location}&start={count}"
    source = make_page_request(url, opts)
    parse(source, BeautifulSoup)
    count += 10
    print(f'Scraped page {i}')

df = pd.DataFrame(master_list)
df.to_csv(f'{search_term}.csv', index=False)

print(f"Total Scraped {len(master_list)} items")
