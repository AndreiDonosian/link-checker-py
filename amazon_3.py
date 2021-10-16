from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import mysql.connector


URLAmazon = 'https://www.amazon.com/Avanchy-Bamboo-Petite-Family-Collections/dp/B08LKDPQP5'
#page = requests.get(URLAmazon)

#soup = BeautifulSoup(page.content, 'html.parser')

class AmazonPars:
    content = ''
    db = []
    cursor = []
    def star_request(self,url):
        if(self._connect()):
            page = requests.get(url)
            self.content = BeautifulSoup(page.content, 'html.parser')
            print(self.content.prettify())
            #self.collect_info()
    def _connect(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="zazir",
            password="0P9o8i7u@",
            #port="8819",
            database="parsamaz"
        )
        if(mydb):
            self.db = mydb
            self.cursor = mydb.cursor(buffered=True)
            return True
        else:
            return False
    
    def collect_info(self):
        print(self._get_title())
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('title','%s')" % (self._get_title()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('price','%s')" % (self._get_price()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('main_image','%s')" % (self._get_main_image()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('alter_images','%s')" % (self._alter_images()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('descr','%s')" % (self._get_descriptionHtml()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('variations','%s')" % (self._get_variation()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('rating','%s')" % (self._get_rating()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('view_number','%s')" % (self._get_review_number()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('asin','%s')" % (self._get_asin()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('rank','%s')" % (self._get_rank()))
        self.cursor.execute("INSERT INTO info_data (field_name,field_value) VALUES ('tech','%s')" % (self._get_techpart()))
        self.db.commit()
        self.db.close()


    def _get_title(self):
        return self.content.find(id="productTitle").text.strip()

    def _get_price(self):
        return self.content.find(id='priceblock_ourprice').text
    
    def _get_main_image(self):
        return self.content.find(id='imgTagWrapperId').find('img').get('src')
    
    def _alter_images(self):
        imgs = []
        for z in self.content.find(id='altImages').find_all('img'):
            imgs.append(z.get('src'))
        return ','.join(imgs)

    def _get_descriptionHtml(self):
        return self.content.find(id='aplus').prettify()

    def _get_bullets(self):
        return self.content.find(id='feature-bullets').prettify()

    def _get_variation(self):
        return self.content.find(id='twisterContainer').prettify()

    def _get_rating(self):
        return self.content.find(id='averageCustomerReviews').find('span').find('span').find('span').find('a').find('i').find('span').text

    def _get_review_number(self):
        return self.content.find(id='acrCustomerReviewText').text

    def _get_asin(self):
        return self.content.find(id='productDetails_detailBullets_sections1').find('tr').find('td').find(class_='prodDetAttrValue').text.strip()

    def _get_rank(self):
        return self.content.find(id='productDetails_detailBullets_sections1').select('tr:nth-child(3)').prettify()

    def _get_techpart(self):
        return self.content.find(id='productDetails_techSpec_section_1').get()

z = AmazonPars()
z.star_request(URLAmazon)