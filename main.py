import requests
from bs4 import BeautifulSoup
from lxml import etree
import lxml.html
import lxml.etree
import csv
import time
from datetime import datetime


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
cur_data = datetime.now().strftime("%d_%m_%y")

def get_data_html():
    urls = []
    count = 0
    for page in range(1, 5):
        url = f"https://www.commercialcafe.com/commercial-real-estate/us/?MapView=true&Page={page}"
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find("div", id="results").find("ul", class_="listings").find_all("h2", class_="building-name")
        for i in items:
            item_link = i.find("a").get('href')
            count +=1
            print(count, item_link)
            urls.append(item_link)
        with open("sourse_page.txt", "w") as file:
            for url in urls:
                file.write(f"{url}\n")
        print(f"Collected page: {page}")


def get_data(file_path="sourse_page.txt"):
    global item_City, item_address, item_Neighborhood, item_Market, item_zipcode, ST, LR, SA
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]  ##Сокращенный вариант
        urls_count = len(urls_list)
    count = 1
    with open(f'data{cur_data}.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Address",
                "City",
                "Neighborhood",
                "Market",
                "Zip Code",
                "Space type",
                "Total Space Available",
                "Lease Rate"
            )
        )

    for url in urls_list:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        tree = lxml.html.document_fromstring(r.text)
        items = tree.xpath('//*[@id="locationDetails"]/ul/li[1]/span/text()')
        try:
            item_address = tree.xpath('normalize-space(//*[@id="detailsSection"]/div[2]/h2/text())')
            print(item_address)
        except:
            item_address = None
            print(item_address)

        try:
            item_City = tree.xpath('normalize-space(/html/body/div[1]/div[6]/div[2]/div[1]/section[3]/div[2]/ul/li[1]/span/text())')
            print(item_City)
        except:
            item_City = None
            print(item_City)

        try:
            item_Neighborhood = tree.xpath('normalize-space(//*[@id="locationDetails"]/ul/li[2]/span/text())')
            print(item_Neighborhood)
        except:
            item_Neighborhood = None
            print(item_Neighborhood)

        try:
            item_Market = tree.xpath('normalize-space(//*[@id="locationDetails"]/ul/li[4]/span/text())')
            print(item_Market)
        except:
            item_Market = None
            print(item_Market)

        try:
            item_zipcode = tree.xpath('normalize-space(//*[@id="locationDetails"]/ul/li[3]/span/text())')
            print(item_zipcode)
        except Exception as _ex:
            item_zipcode = None
            print(item_zipcode)

        try:
            item_spacetypeA = tree.xpath('normalize-space(//*[@id="939299"]/div/section[1]/ul/li[1]/span/text())')
            item_spacetypeB = tree.xpath('normalize-space(//*[@id="939300"]/div/section[1]/ul/li[1]/span/text())')
            item_spacetypeC = tree.xpath('normalize-space(//*[@id="939301"]/div/section[1]/ul/li[1]/span/text())')
            print(item_spacetypeA,item_spacetypeB,item_spacetypeC)
        except:
            item_spacetypeA, item_spacetypeB, item_spacetypeC = None
            print(item_spacetypeA,item_spacetypeB,item_spacetypeC)

        ST = [item_spacetypeA, item_spacetypeB, item_spacetypeC]


        try:
            item_spaceAviableA = tree.xpath('normalize-space(//*[@id="939299"]/div/section[1]/ul/li[3]/span/text())')
            item_spaceAviableB = tree.xpath('normalize-space(//*[@id="939300"]/div/section[1]/ul/li[3]/span/text())')
            item_spaceAviableC = tree.xpath('normalize-space(//*[@id="939301"]/div/section[1]/ul/li[3]/span/text())')
            print(item_spaceAviableA,item_spaceAviableB,item_spaceAviableC)
        except:
            item_spaceAviableA, item_spaceAviableB, item_spaceAviableC = None
            print(item_spaceAviableA,item_spaceAviableB,item_spaceAviableC)

        SA = [item_spaceAviableA, item_spaceAviableB, item_spaceAviableC]



        try:
            item_LR_A = tree.xpath('normalize-space(//*[@id="939299"]/div/section[1]/ul/li[2]/span/text())')
            item_LR_B = tree.xpath('normalize-space(//*[@id="939300"]/div/section[1]/ul/li[2]/span/text())')
            item_LR_C = tree.xpath('normalize-space(//*[@id="939301"]/div/section[1]/ul/li[2]/span/text())')
            print(item_LR_A, item_LR_B, item_LR_C)
        except:
            item_LR_A, item_LR_B, item_LR_C = None
            print(item_LR_A, item_LR_B, item_LR_C)

        LR = [item_LR_A, item_LR_B, item_LR_C]

    with open(f'data{cur_data}.csv', 'a', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                item_address,
                item_City,
                item_Neighborhood,
                item_Market,
                item_zipcode,
                ST, SA, LR
            )
         )

def main():
    get_data_html()
    get_data(file_path="sourse_page.txt")
    print("[INFO] Data collected successfully")

if __name__ == "__main__":
    main()