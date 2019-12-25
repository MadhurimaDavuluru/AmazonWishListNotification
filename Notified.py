import requests,time,smtplib
from bs4 import  BeautifulSoup
from notify_run import Notify
from datetime import datetime
import re

'''
url = input("Enter your URL here : ")
dp = int(input("Enter your desired price : "))
'''
#-----------------------------------------------
url = "https://www.amazon.in/hz/wishlist/ls/11FEYGW3WLGSN?&sort=default"
dp = 500
URL = url
pnmsg = "Hey Ron! Get your "
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
 
def check_price():
  
 
  page = requests.get(URL, headers=headers)
  soup= BeautifulSoup(page.content,'html.parser')
  #----------------------------------------------------- TO CHECK WHETHER soup IS WORKING OR NOT
  '''
  m=open('soupw.txt',"wb")
  m.write(soup.prettify().encode("utf-8"))
  m.close
  '''
  #--------------------------------------------------------------------------------------
  html_items = soup.findAll(id= re.compile("^itemInfo_"))
  titles=[]
  prices=[]
  totalItems=0
  for i, html_item in enumerate(html_items):
    totalItems+=1
  for i, html_item in enumerate(html_items):
    titles.append(html_item.find(id=re.compile("^itemName_")).get_text().strip())
    price=html_item.find(id=re.compile("^itemPrice_")).get_text().strip()
    prices.append(int(re.findall("[0-9]+",price)[0]))
    print("NAME : "+ titles[i])
    print("CURRENT PRICE : "+ str(prices[i]))
    print("DESIRED PRICE : "+ str(dp))
 
  #-----------------------------------------------Temporary fixed for values under Rs.  9,999
  #FUNCTION TO CHECK THE PRICE-------------------------------------------------------
  count = 0
  for i in range(totalItems):
    
    if(prices[i] <= dp): 
      send_mail(titles[i],prices[i]) 
      push_notification(titles[i],prices[i])
    else:
      count = count+1
    print("Rechecking... Last checked at "+str(datetime.now()))
  
 
#Lets send the mail-----------------------------------------------------------------
def send_mail(title,price):
  server = smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login('YourSMTPmail','Password')
  subject = "Price of "+title+" has fallen down below Rs. "+str(dp)
  body = "Hey Ron! \n The price of "+title+" on AMAZON has fallen down below Rs."+str(dp)+".\n So, hurry up & check the amazon link right now : "+url
  msg = f"Subject: {subject} \n\n {body} "
  server.sendmail(
  'YourSMTPmail',
  'TheAccountMailYouWantToRecieveNotification',
  msg
  )
  print("Email sent-Success")
 
  server.quit()
#Now lets send the push notification-------------------------------------------------
def push_notification(title,price):
  notify = Notify()
  notify.send(pnmsg+title+" on Amazon for price of Rs."+str(price))
  print("Push notification-Success")
 
  print("Check again after an hour.")
#Now lets check the price after 1 min ----------------------------------------------- 
count = 0
while(True):
  count += 1
  print("Count : "+str(count))
  check_price()
  time.sleep(3600)
#but demonstration purpose I entered 5 instead of 3600 in line no 111
