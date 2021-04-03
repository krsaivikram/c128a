from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import requests
starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:/Users/Manorama/Desktop/c127/chromedriver")
browser.get(starturl)
time.sleep(10)
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]

planet_data = []
newplanetdata = []
def Scrap():
    for i in range(1,430):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentpagenumber = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
            if currentpagenumber<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpagenumber>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break  
    for ul_tag in soup.find_all("ul",attrs = {"class","exoplanet"}):
        li_tags = ul_tag.find_all("li")
        temp_list = []
        for index,li_tag in enumerate(li_tags):
            if index==0:
                temp_list.append(li_tag.find_all("a")[0].contents[0])
            else:
                try:
                    temp_list.append(li_tag.contents[0])
                except:
                    temp_list.append("")
        hyperlink_litag = li_tags[0]
        temp_list.append("https://exoplanets.nasa.gov"+hyperlink_litag.find_all("a",href = True)[0]["href"])
        planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
        print(f"{i}page done 1")
def Scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        newplanetdata.append(temp_list)
    except:
        time.sleep(1)
        Scrapmoredata(hyperlink)
Scrap()
for index,data in enumerate(planet_data):
    Scrapmoredata(data[5])
    print(f"{index+1}page done 2")
finalplanetdata = []
for index,data in enumerate(planet_data):
    newplantedataelement = newplanetdata[index]
    newplanetdataelement = [elem.replace("\n","")for elem in newplanetdataelement]
    newplanetdataelement = newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)
with open("final.csv","w")as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)

