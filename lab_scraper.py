import requests
import json
import bs4
import csv


def lab_scraper(url):
    url = "https://www.labuncle.com/lab-partners"
    res = requests.get(url)
    res = res.text
    data = bs4.BeautifulSoup(res, "html.parser")

    rd = data.select(".lab-list")  # get all the lab list
    x = rd[0].find_all("a")
    lab_url = []
    for i in range(len(x)):
        lab_url.append(x[i].get("href"))  # append all the lab url in to lsit

    for i in range(1, 36):
        # url=f"https://www.labuncle.com{lab_url[i]}"
        res = requests.get(f"https://www.labuncle.com{lab_url[i]}")  # get each lab's data
        res = res.text
        data = bs4.BeautifulSoup(res, "html.parser")

        name = data.find_all('h1', {'class': 'bann-heading'})
        address = data.find_all('span', {'class': 'ban-lab-add'})
        discount = data.find_all('div', {'class': 'banner-discount'})
        ph_no = data.find_all('a', {'class': 'btn btn-default float-left float-md-none mx-md-4 mt-4'})
        lab_facilities = data.find_all('ul', {'class': "lab-faci"})
        lab_fac = []
        d = " "
        if len(discount) > 0:
            d = discount[0].text
        for i in range(len(lab_facilities)):
            x = lab_facilities[i].find_all("li")
            for j in range(len(x)):
                y = x[j].find_all("a")
                lab_fac.append(y[0].text)

        item = {
            'name': name[0].text,
            'address': address[0].text,
            'Discounted_Price': d,
            'Phone_no': ph_no[0].get("href"),
            'test_included': lab_fac
        }
        with open("output3.csv", 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            writer.writerow(item)


lab_scraper('https://www.labuncle.com')