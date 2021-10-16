import scrapy
import random

class ProxiScrapper(scrapy.Spider):
    name = 'proxies'
    start_urls = ['https://www.amazon.com/gp/product/B00A037VHM']
    proxy_urls = ['https://free-proxy-list.net']
    proxyList = []
    proxyBlackList = []
    proxyUsedList = []
    #collecting proxies

    def start_requests(self):
        for url in self.start_urls:
            if(len(self.proxyList)<5):
                yield scrapy.Request(url = self.proxy_urls[0], callback = self.parse_proxy)

    def parse(self, response):
        for item in response.css('.a-color-price .p13n-sc-price'):
            yield item.get()
            
        print(self.proxyList,'aaaaaa')

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)

    def parse_proxy(self, response):
        # print(response.css('.table-striped tbody>tr').get(),"ZZZZZZZZ")
        # z = ''
        for ips in response.css('.table-striped tbody>tr'):
            proxyString = self._tag_replacer(ips.css('td')[0].get(),'td')+":"+self._tag_replacer(ips.css('td')[1].get(),'td')
            # print(proxyString,"ZZZZZZZZ",self._tag_replacer(ips.css('td')[6].get(),'td',' class="hx"'))
            if(self._tag_replacer(ips.css('td')[6].get(),'td',' class="hx"')=='yes' and proxyString not in self.proxyBlackList):#https only proxy
                z = self._test_proxy(self._tag_replacer(ips.css('td')[0].get(),'td')+":"+self._tag_replacer(ips.css('td')[1].get(),'td'))
                #self.proxyList.append(self._tag_replacer(ips.css('td')[0].get(),'td')+":"+self._tag_replacer(ips.css('td')[1].get(),'td'))
            if(len(self.proxyList)>5):
                break
        print(self.proxyList,'bbbbbbbbb')
        if(len(self.proxyList)>5):
            randProxyIndx = random.randint(0, 4)
            print(self.proxyList,'zzz')
            yield scrapy.Request(url=url, callback=self.parse,
                       headers={"User-Agent": "My UserAgent"},
                       meta={"proxy": "https://"+self.proxyList[randProxyIndx]},
                       errback=self._blacklist_proxy,
                       )

    def _tag_replacer(self, string, tag, additional = ''):
        return string.replace('<'+tag+additional+'>',"").replace('</'+tag+'>',"")

    def _test_proxy(self, proxy):
        yield scrapy.Request(self.proxy_urls[0], meta={"proxy":"https://"+proxy}, callback=self._save_proxy, cb_kwargs=dict(proxy=proxy), errback=self._blacklist_proxy)
    
    def _save_proxy(self, response, proxy):
        print('ccccccccc',proxy)
        yield self.proxyList.append(proxy)
    
    def _blacklist_proxy(self, failure):
        for z in self.proxyList:
            if(self.proxyList[z]==failure.request.cb_kwargs['proxy']):
                self.proxyBlackList.append(failure.request.cb_kwargs['proxy'])
                yield self.proxyList.pop(z)