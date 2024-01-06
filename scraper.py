import requests
import bs4
import csv
import json


def scrape_pharmeasy_data(url):
# ......................................................................................................
    url = f"https://pharmeasy.in/api/home/fetchCategories"    ##get all the categories
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []
    categorie=[];
    res=json.loads(response.content)
    for i in res["data"]["categories"]:
      categorie.append(i["id"])
    data=[]
# ......................................................................................................
    for cat in categorie:
      for j in range(1,40):
        url=f"https://pharmeasy.in/api/otc/getCategoryProducts?categoryId={cat}&page={j}"
        # print(url)
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to retrieve the webpage")
            return []

        res=json.loads(response.content)

        for i in res["data"]["products"]:
          if i['name'][0]=='B' or i['name'][0]=='F'or i['name'][0]=='b' or i['name'][0]=='f':
            pid=i["productId"]
            url_j=f"https://pharmeasy.in/health-care/products/{pid}"
            item={
              'name':i['name'],
              'mrp':i["mrpDecimal"],
              'url_j':url_j,
              'Discounted_Price':i["discountDecimal"],
              'manufacturer':i["manufacturer"],
            }
            with open ("output1.csv", 'a') as csv_file:
              writer=csv.DictWriter(csv_file,fieldnames=item.keys())
              writer.writerow(item)


def scrape_netmeds_data(url):
  url=f"https://www.netmeds.com/prescriptions"
  res = requests.get(url)
  res=res.text
  data=bs4.BeautifulSoup(res,"html.parser")
  rd=data.select(".alpha-drug-list")
  co_url=[]
  print(len(rd))
  for i in range(len(rd)):
    x=rd[i].find_all("li")
    for j in range(len(x)):
      y=x[j].find_all("a")
      co_url.append(y[0].get("href"))

  all_url=[]
  for i in range(1,10):
    res = requests.get(co_url[i])
    res=res.text
    data=bs4.BeautifulSoup(res,"html.parser")
    rd=data.select(".panel-body")
    # print(rd)
    for i in range(len(rd)):
      x=rd[i].find_all("li")
      for j in range(len(x)):
        y=x[j].find_all("a")
        all_url.append(y[0].get("href"))

  for i in range(1,600):
    res = requests.get(all_url[i])
    res=res.text
    data=bs4.BeautifulSoup(res,"html.parser")
    # print(data.find_all('base'))

    med_name=data.find_all('h1',{'class':'black-txt'})

    if med_name!=[]:
      if med_name[0].text[0]=='B' or med_name[0].text[0]=='F':
        med_name=data.find_all('h1',{'class':'black-txt'})
        med_price=data.find_all('span',{'class':'final-price'})
        med_dis=data.find_all('span',{'id':'barBestPrice'})
        med_man=data.find_all('div',{'class':"manufacturer__name_value"})
        med_url=all_url[i];
        if len(med_man)==0:
          med_man=""
        else:
          med_man=med_man[len(med_man)-1].text


        if len(med_dis)==0:
          med_dis=""
        else:
          x=med_dis[len(med_dis)-1].text
          # print(len(med_des))

        item={
                  'name':med_name[0].text,
                  'mrp':med_price[0].text,
                  'url_j':med_url,
                  'Discounted_Price':x,
                  'manufacturer':med_man,
          }
        with open ("output1.csv", 'a') as csv_file:
          writer=csv.DictWriter(csv_file,fieldnames=item.keys())
          writer.writerow(item)


scrape_netmeds_data("https://www.netmeds.com/prescriptions")
scrape_pharmeasy_data("https://pharmeasy.in/api/home/fetchCategories")