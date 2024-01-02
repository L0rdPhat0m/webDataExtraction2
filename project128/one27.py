from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
import requests


start_url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'
browser = webdriver.Chrome("/Users/anugu/Downloads/chromedriver_win32/chromedriver.exe")
browser.get(start_url)
time.sleep(10)
scraped_data=[]
headers = ["STAR-NAME","DISTANCE","MASS","RADIUS","LUMINOSITY"]
new_planet_data =[]
planet_data = []

def scrape():
    
    planets_data = []
    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for th_tag in soup.find_all("th",attrs={"class","exoplanet"}):
            td_tag = td_tag.find_all("td")
            tempt_list = []
            for index,td_tag in enumerate(td_tag):
                if index == 0:
                    tempt_list.append(td_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        tempt_list.append(td_tag.contents[0])
                    except:
                        tempt_list.append("")
            planets_data.append(tempt_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scraper_2.csv","w") as z:
        csv_writer = csv.writer(z)
        csv_writer.writerow(headers)
        csv_writer.writerows(planets_data)

def scrapeMoreData(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrapeMoreData(hyperlink)
scrape()
for index, data in enumerate(planet_data):
    scrapeMoreData(data[5])
    print(f"{index+1} page done 2")
final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)