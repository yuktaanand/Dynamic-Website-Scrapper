import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
with open('innovatorssss.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Recipe Name","Reviewer Name","Review","Review Date","Rating"]) # remove it after first url
    url = 'https://www.allrecipes.com/recipes/22959/healthy-recipes/keto-diet/?internalSource=hubcard&referringContentType=Search&clickId=cardslot&201'
    # url = 'https://www.allrecipes.com/recipes/22959/healthy-recipes/keto-diet/?internalSource=hubcard&referringContentType=Search&clickId=cardslot%201&page=24' # for page 2 to 24
    response = requests.get(url)

    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    results=soup.find_all('h3', class_="fixed-recipe-card__h3")
    reviewer_name=list()
    review_detail=list()
    review_date = list()
    name_list=list()
    rating=list()
    print(len(results))
    flag=0
    
    for x in range(0,len(results)):
        flag=0
        recipe_url = results[x].find('a')['href']
        print(recipe_url)
        number_of_reviews=0
        response1 = requests.get(recipe_url)
        html1 = response1.content
        soup1 = BeautifulSoup(html1, 'html.parser')
        number_of_review=""
        if(len(soup1.find_all('a', class_="ugc-ratings-link ugc-reviews-link"))!=0):
          reviews = soup1.find('a', class_="ugc-ratings-link ugc-reviews-link").text.strip()
          for g in range(0,len(reviews)):
            if(reviews[g]==' '):
              break
            else:
              number_of_review += reviews[g]
          number_of_reviews = int(number_of_review)
        elif(soup1.find('span',class_="review-count")!=None):
          reviews = soup1.find('span',class_="review-count").text.strip()
          for g in range(0,len(reviews)):
            if(reviews[g]==' '):
              break
            else:
              number_of_review += reviews[g]
          number_of_reviews = int(number_of_review)
        print(number_of_reviews)
        if(number_of_reviews!=0):
          driver = webdriver.Chrome('/home/yukta_anand/Downloads/chromedriver_linux64/chromedriver')
          driver.get(recipe_url)
          if(soup1.find('span',class_="review-count")!=None):
            
            ele = driver.find_element_by_xpath('//*[@id="main-content"]/div[3]/section/div[1]/div/section[2]/div[3]/div/span[1]/a/span[4]')
            ele.click()
            if(number_of_reviews==1):
              flag=1
            flag1=0
            while(number_of_reviews>0):
              
              res=driver.page_source
              soup = BeautifulSoup(res, 'html.parser')
              review_modal = soup.find('div', class_="reviewModalTextColumn")
              if(flag1==1):
                reviewer_name.append(review_modal.find('h4',class_="ng-binding").text.strip())
                review_detail.append(review_modal.find('p',class_="ReviewText ng-binding").text.strip())
              
                review_date.append(review_modal.find('i', class_="ng-binding").text.strip())
                rating.append("5")
                recipe_name=results[x].find('span', class_='fixed-recipe-card__title-link')
                name_list.append(recipe_name.text.strip())
              flag1=1
              ele = driver.find_element_by_xpath('//*[@id="BI_loadReview1_right"]')
              number_of_reviews=number_of_reviews-1
              if(number_of_reviews>0):
                ele.click()
            driver.quit()  
            
        else:
            recipe_name=results[x].find('span', class_='fixed-recipe-card__title-link')
            name_list.append(recipe_name.text.strip())
            reviewer_name.append("None")
            review_detail.append("None")
            review_date.append("None")
            rating.append("0")
    for i in zip(name_list,reviewer_name,review_detail,review_date,rating):
        writer.writerow(i)
