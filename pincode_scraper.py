import requests
import csv
import bs4

def scrape_medicine_availability(pincode , url):
  delivery_date=""
  cookie={
    "etaPincode":f"{pincode}",
  }
  res = requests.get(url,cookies=cookie)
  res=res.text
  data=bs4.BeautifulSoup(res,"html.parser")
  rd=data.find_all('span')
  # print(len(rd))
  count=0
  flag=0
  for i in rd:
    if i.text=='Earliest delivery by':
      flag=1
      count+=1
      break
    count+=1
  if flag==0:
    print("pincode not correct")
  else:
    delivery_date=rd[count].text
    # print(rd[count].text)
  return {'delivery_date':delivery_date,'pincode':pincode,'url':url}


x=scrape_medicine_availability("160062","https://www.1mg.com/drugs/azildac-80-tablet-340848?wpsrc=Google+Organic+Search")
print(x)
with open("output2.csv", 'a') as csv_file:
  writer = csv.DictWriter(csv_file, fieldnames=x.keys())
  writer.writerow(x)