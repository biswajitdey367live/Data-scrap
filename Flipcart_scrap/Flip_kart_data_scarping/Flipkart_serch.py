#Downloading Prerequisite
import os
import sys
os.system(f'{sys.executable} -m pip install -r requirements.txt')

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
import requests


class Flipkart():

    def __init__(self):

        self.url = 'https://www.flipkart.com'
        # Chromedriver is just like a chrome. you can dowload latest by it website
        self.driver = webdriver.Chrome(ChromeDriverManager(path="C:\\Users\\BISWA\\PycharmProjects\\tier5\\driver_manager\\").install())

    def page_load(self):

       self.driver.get(self.url)
       self.driver.maximize_window()
       self.driver.implicitly_wait(50)

       try:
            #login_pop = self.driver.find_element_by_class_name('_2KpZ6l _2doB4z')
            login_pop=self.driver.find_element_by_xpath("/html/body/div[2]/div/div/button")
            # Here .click function use to tap on desire elements of webpage
            login_pop.click()
            print('pop-up closed')
       except:
            pass

       # Search field  class name from web
       search_field = self.driver.find_element_by_class_name('_3704LK')


       # Search keyword which trying to search
       search_field.send_keys('iphone11' + '\n')
       self.driver.find_element_by_class_name("L0Z3Pu").click()

       # Here time.sleep is used to add delay for loading context in browser
       time.sleep(3)
       self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div[1]/div[1]/div/div/div/div/section/div[2]/div[2]/a[1]').click()


       #sorting price low to high
       self .driver.find_element_by_xpath("//*[contains(text(),'Price -- Low to High')]").click()

       #Current URL
       URL = self.driver.current_url
       page = requests.get(URL)



       # Here BeautifulSoup is dump page source into html format
       self.soup = BeautifulSoup(page.content, 'html.parser')

    #Function for CSV creation
    def create_csv_file(self):

        # Here I have created CSV file with desired header.
        rowHeaders = ["Name", "Price in Rupees", "Ratings"]
        self.file_csv = open('Flipkart_output.csv', 'w', newline='', encoding='utf-8-sig')
        self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
        # Writeheader is pre-defined function to write header
        self.mycsv.writeheader()

    def data_scrap(self):

        # Here I fetch all products div elements
        results = self.soup.find_all("div",{"class":'_1AtVbE col-12-12'})


        for i in results:
            if i.find(class_='_4rR01T') and i.find("div", {"class": '_3LWZlK'}) and i.find("div", {
                "class": '_30jeq3 _1_WHN1'}):
                name = i.find(class_='_4rR01T').text
                rating = i.find("div", {"class": '_3LWZlK'}).text
                price = i.find("div", {"class": '_30jeq3 _1_WHN1'}).text

                self.mycsv.writerow({"Name": name, "Price in Rupees": price, "Ratings": rating})

            else:
                name = ""

    def tearDown(self):

        # Closing all active tab
        self.driver.quit()

        # Closing csv file which opened

        self.file_csv.close()

if __name__ == "__main__":

    Flipkart = Flipkart()
    Flipkart.page_load()
    Flipkart.create_csv_file()
    Flipkart.data_scrap()
    Flipkart.tearDown()
    print("All data has been retrieved")