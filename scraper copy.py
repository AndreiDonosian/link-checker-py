import scrapy
import mysql.connector
import html
from PIL import Image

class ProxiScrapper(scrapy.Spider):
    name = 'proxies'
    start_urls = ['https://ifconfig.me/ua']
    cursor = {}
    cursor_insert = {}
    proxyList = {}
    db = []
    cursor = []

    custom_settings = {
        'RETRY_TIMES': 34,
        'RETRY_HTTP_CODES': [500,503, 504, 400, 403, 404, 408],
        'DOWNLOAD_TIMEOUT': 7,

        # 'DOWNLOADER_MIDDLEWARES' : {
        #     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        #     'scrapy_proxies.RandomProxy': 100,
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        #     # 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':120,
        #     # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        #     # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        # },
        # 'PROXY_LIST': '/var/www/html/amz/proxy2.txt',
        # 'PROXY_MODE': 0,
        # 'CUSTOM_PROXY':"http://93.177.116.173:8085"
        # 'USER_AGENTS' : [
        #     ('Mozilla/5.0 (X11; Linux x86_64) '
        #     'AppleWebKit/537.36 (KHTML, like Gecko) '
        #     'Chrome/57.0.2987.110 '
        #     'Safari/537.36'),  # chrome
        #     ('Mozilla/5.0 (X11; Linux x86_64) '
        #     'AppleWebKit/537.36 (KHTML, like Gecko) '
        #     'Chrome/61.0.3163.79 '
        #     'Safari/537.36'),  # chrome
        #     ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        #     'Gecko/20100101 '
        #     'Firefox/55.0'),
        #     ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4453.0 Safari/537.36')  # firefox
        # ],
        # 'RANDOM_UA_PER_PROXY': True,
        # 'RANDOM_UA_TYPE': 'desktop',
        # 'ITEM_PIPELINES' : {'scrapy.pipelines.images.ImagesPipeline': 1},
        # 'IMAGES_STORE' : '/var/www/html/basic/web/downloaded_content'
    }
    

    def start_requests(self):
        if(self._connect()):
            self.cursor.execute('SELECT * from to_parse where today_parsed=0 and (last_parsed<DATE(NOW()) or last_parsed is null) LIMIT 10')#limiting to 10
            for urls in self.cursor.fetchall():
                try:
                    yield scrapy.Request(str(urls[1]),self.parse,
    errback=self.err_parse) #link attr
                except:
                    self.cursor_insert.execute("UPDATE to_parse set today_parsed=2 WHERE link='%s'" %(str(urls[1])))

    def err_parse(self, failure):
        self.cursor_insert.execute("UPDATE to_parse set today_parsed=3 WHERE link='%s'" %(str(failure.request.url)))

    def parse(self, response):
        # print(response.css('html').get())
        tech_dimension = ''
        tech_item_weight = ''
        tech_manufacturer = ''
        tech_model_number = ''
        tech_target_gender = ''
        tech_material_type = ''
        tech_material_composition = ''
        tech_style = ''
        tech_material_free = ''
        tech_care_instructions = ''
        tech_battery_req = ''
        rank = ''
        tech_is_discontinued = ''
        tech_date_first_available = '1990-03-27 18:14:24'
        feature_material = ''
        feature_color = ''
        feature_brand = ''
        feature_item_weight = ''
        feature_capacity = ''
        feature_item_dimension = ''
        feature_item_dimension_l_w_h = ''
        if(self.cursor_insert):
            print("BEFORE ASIIIIIIN")
            asin = self._get_asin(response)
            print("ASSIIIN", asin)
            if(asin is not None):
                asin = str(asin).strip()
                print("STAAAAAART")
                title = self.html_escape(str(self._get_title(response)))
                price = self.html_escape(str(self._get_price(response)))
                alter_images = self.html_escape(str(self._alter_images(response)))
                descr = self.html_escape(self._get_descriptionHtml(response))
                bullets = self.html_escape(str(self._get_bullets(response)))
                variations = self.html_escape(str(self._get_variation(response)))
                rating = self.html_escape(str(self._get_rating(response)))
                rating_number = self.html_escape(str(self._get_review_number(response)))

                tech_part = self.scan_tech_part(response,asin)

                if('tech_dimension'  in tech_part.keys()):
                    tech_dimension = tech_part['tech_dimension']

                if('tech_item_weight'  in tech_part.keys()):
                    tech_item_weight = tech_part['tech_item_weight']

                if('tech_manufacturer'  in tech_part.keys()):
                    tech_manufacturer = tech_part['tech_manufacturer']

                if('tech_model_number'  in tech_part.keys()):
                    tech_model_number = tech_part['tech_model_number']

                if('tech_target_gender'  in tech_part.keys()):
                    tech_target_gender = tech_part['tech_target_gender']

                if('tech_material_type'  in tech_part.keys()):
                    tech_material_type = tech_part['tech_material_type']

                if('tech_material_composition'  in tech_part.keys()):
                    tech_material_composition = tech_part['tech_material_composition']

                if('tech_style'  in tech_part.keys()):
                    tech_style = tech_part['tech_style']

                if('tech_material_free'  in tech_part.keys()):
                    tech_material_free = tech_part['tech_material_free']
                
                if('tech_care_instructions'  in tech_part.keys()):
                    tech_care_instructions = tech_part['tech_care_instructions']

                if('tech_battery_req'  in tech_part.keys()):
                    tech_battery_req = tech_part['tech_battery_req']

                if('rank'  in tech_part.keys()):
                    rank = tech_part['rank']

                if('tech_is_discontinued'  in tech_part.keys()):
                    tech_is_discontinued = tech_part['tech_is_discontinued']

                if('tech_date_first_available'  in tech_part.keys()):                
                    tech_date_first_available = tech_part['tech_date_first_available']
        
                feature_part = self.scan_feature_part(response,asin)

                if('feature_material'  in feature_part.keys()):
                    feature_material = feature_part['feature_material']

                if('feature_color'  in feature_part.keys()):
                    feature_color = feature_part['feature_color']

                if('feature_brand'  in feature_part.keys()):
                    feature_brand = feature_part['feature_brand']

                if('feature_item_weight'  in feature_part.keys()):
                    feature_item_weight = feature_part['feature_item_weight']

                if('feature_capacity'  in feature_part.keys()):
                    feature_capacity = feature_part['feature_capacity']
                
                if('feature_item_dimension'  in feature_part.keys()):
                    feature_item_dimension = feature_part['feature_item_dimension']

                if('feature_item_dimension_l_w_h'  in feature_part.keys()):
                    feature_item_dimension_l_w_h = feature_part['feature_item_dimension_l_w_h']

                self.cursor_insert.execute('INSERT INTO parsed_data_items (asin,title, price, alter_images, descr, bullets, variations, rating, rating_number, tech_dimension, tech_model_number, tech_target_gender, tech_material_type, tech_material_free, tech_care_instructions, tech_battery_req, tech_item_weight, tech_manufacturer, tech_is_discontinued, tech_date_first_available, tech_material_composition, tech_style, rank, feature_material, feature_color, feature_brand, feature_item_weight, feature_capacity, feature_item_dimension_l_w_h) VALUES'
                    '("%s","%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' %(asin,title, price, alter_images, descr, bullets, variations, rating, rating_number, tech_dimension, tech_model_number, tech_target_gender, tech_material_type, tech_material_free, tech_care_instructions, tech_battery_req, tech_item_weight, tech_manufacturer, tech_is_discontinued, tech_date_first_available, tech_material_composition, tech_style, rank, feature_material, feature_color, feature_brand, feature_item_weight, feature_capacity, feature_item_dimension_l_w_h))
                    
                self.cursor_insert.execute("UPDATE to_parse set today_parsed=1, last_parsed=NOW() WHERE link='%s'" %(str(response.url))) #(title, price, alter_images, descr, bullets, variations, rating, rating_number, tech_dimension, tech_model_number, tech_target_gender, tech_material_type, tech_material_free, tech_care_instructions, tech_battery_req, tech_item_weight, tech_manufacturer, tech_is_discontinued, tech_date_first_available, tech_material_composition, tech_style, rank, feature_material, feature_color, feature_brand, feature_item_weight, feature_capacity, feature_item_dimension_l_w_h)
               

                self.db.commit()
            else:
                print(response.css('html').get().encode('utf-8'))
            
    
    def html_escape(self,text):
        html_escape_table = {
        "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }
        if(text):
            return "".join(html_escape_table.get(c,c) for c in text)
        else:
            return None

    def _connect(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="zazir",
            password="0P9o8i7u@",
            # port="8819",
            database="parsamaz"
        )
        if(mydb):
            self.db = mydb
            self.cursor = mydb.cursor()
            self.cursor_insert = mydb.cursor()
            return True
        else:
            return False

    def _tag_replacer(self, string, tag):
        return string.replace('<'+tag+'>',"").replace('</'+tag+'>',"")

    def _get_title(self, response):
        z = response.css('#productTitle::text').get()
        if(z is None):
            f = response.css('#title::text').get()
            if f is not None:
                return f.encode('utf-8').strip()
            else: 
                return None
        else:
            return z.encode('utf-8').strip()

    def _get_price(self, response):
        z = response.css('#priceblock_ourprice::text').get()
        if z is None:
            f = response.css('#priceblock_saleprice::text').get() #response.css('table.a-lineitem tr:nth-child(1) td:nth-child(3) span::text').get()
            if(f):
                return f.strip()
            else:
                e = response.css("#price_inside_buybox::text").get()
                if(e):
                    return e.strip()
                else:
                    return "None"
        else:
            return z.strip()
    # def _get_image(self, response):
    #     return response.css('#imgTagWrapperId>img').get()

    def _alter_images(self, response):
        return ",".join(response.css('#altImages img::attr(src)').getall()).strip()

    def _get_descriptionHtml(self, response):
        z = response.css("#productDescription>p::text").get()
        if z is None:
            f = response.css('#aplus>p::text').get()
            if(f):
                return f.encode("utf8").strip()
            else:
                return "None"
        else:
            return z.encode("utf8").strip()

    def _get_bullets(self, response):
        z = response.css('#feature-bullets>ul>li>span::text').getall()
        if z is None:
            return "None"
        else:
            bulls = []
            for bull in z:
                bulls.append(bull.encode("utf8").strip())
            return "|||".join(bulls)

    def _get_variation(self, response):
        images = response.css('#variation_color_name ul>li img').getall() 
        prices = response.css('#variation_color_name ul >li .twisterSwatchPrice').getall()
        if images is None:
            return response.css('ul.a-unordered-list.a-nostyle.a-button-list.a-declarative.a-button-toggle-group.a-horizontal.dimension-values-list').get()
        else:
            output = ''
            if(images):
                counter = 0
                for key in images:
                    output += "IMG:"+key+"\n"
                for key in prices:
                    output += "|PRICE: "+key+"\n"
            return output

    def _get_rating(self, response):
        z = response.css('#averageCustomerReviews>span>span>span>a>i>span::text').get()
        if z is None:
            return response.css('#averageCustomerReviews_feature_div i.a-icon-star-mini::text').get()
        else:
            return z

    def _get_review_number(self, response):
        return response.css('#acrCustomerReviewText::text').get()

    def _get_asin(self, response):
        z = response.css('#ASIN::attr(value)').get()
        if z is None:
            x = response.css('#productDetails_detailBullets_sections1 > tr > td::text').get() #response.css('#productDetails_detailBullets_sections > li > span span:nth-child(2)::text').get()
            if x is None:
                return None
            else:
                return x
        else:
            return z

    def _get_rank_total(self, response):
        return response.css('#acrCustomerReviewText::text').get()

    def scan_feature_part(self, response, asin):
        feature_part = {}
        for z in response.css("#productOverview_feature_div table tr"):
            title = z.css("td:nth-child(1)>span::text").get()
            key = ''
            val = ''
            if(title):
                title = title.strip()
                if(title=='Material'):
                    key='feature_material'
                if(title=='Color'):
                    key='feature_color'
                if(title=='Brand'):
                    key='feature_brand'
                if(title=='Item Weight'):
                    key='feature_item_weight'
                if(title=='Capacity'):
                    key='feature_capacity'
                if(title=='Item Dimensions'):
                    key= 'feature_item_dimension'
                if(title=='Item Dimensions LxWxH'):
                    key= 'feature_item_dimension_l_w_h'

                if(key):
                    feature_part[key] = self.html_escape(str(z.css("td:nth-child(2)>span::text").get().strip()))
        return feature_part



    
    def scan_tech_part(self, response, asin):
        # tech_part = dict()
        return self._parse_tech_part(response, asin)

    def _parse_tech_part(self, response,asin):
        tech_part = dict()
        for rows in response.css("#productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr"):
            title = rows.css("th::text").get()
            key=''
            getall = False
            val = ''

            if(title is not None):
                title = title.strip()
                if(title=='Product Dimensions' or title=='Package Dimensions'):
                    key = 'tech_dimension'

                if(title=='Item Weight'):
                    key = 'tech_item_weight'

                if(title=='Manufacturer'):
                    key = 'tech_manufacturer'

                if(title=='Item model number'):
                    key = 'tech_model_number'

                if(title=='Target gender'):
                    key = 'tech_target_gender'

                if(title=='Material Type'):
                    key = 'tech_material_type'

                if(title=='material_composition'):
                    key = 'tech_material_composition'

                if(title=='Style'):
                    key = 'tech_style'

                if(title=='Material free'):
                    key = 'tech_material_free'
                
                if(title=='Care instructions'):
                    key = 'tech_care_instructions'

                if(title=='Batteries required'):
                    key = 'tech_battery_req'

                # if(title=='Customer Reviews'):
                #     key = 'rating'

                if(title=='Best Sellers Rank'):
                    key = 'rank'
                    getall = True

                if(title=='Is Discontinued By Manufacturer'):
                    key = 'tech_is_discontinued'

                if(title=='Date First Available'):
                    key = 'tech_date_first_available'

                if(key):
                    if(getall):
                        if(key=='rank'):
                            val = self.html_escape(str("|||".join(rows.css("td>span>span::text,td>span>span>a::text").getall()).strip()))
                        else:
                            val = self.html_escape(str(rows.css("td").get().strip()))
                    else:
                        val = self.html_escape(str(rows.css("td::text").get().strip()))
                    
                    tech_part[key] = val

        return tech_part
