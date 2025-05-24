import scrapy
import datetime
from urllib.parse import urlencode
 

class EbayproductsSpider(scrapy.Spider):
    name = "ebayproducts"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com/sch/i.html?_nkw=COCCINELLE&_sacat=0&_from=R40&_ipg=240"]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search_page, meta = {'impersonate': 'chrome'})

    def parse_search_page(self, response):
        products =  products = response.css('ul.srp-results.srp-grid.clearfix li.s-item__pl-on-bottom')
        for product in products:
            product_url = product.css('div.s-item__image a::attr(href)').get()
            if 'COCCINELLE' in str(product_url):
                yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta = {'impersonate': 'chrome'})
        
            next_page = response.css('div.s-pagination a.pagination__next.icon-link::attr(href)').get()
            if  next_page is not None:
                yield response.follow(next_page, self.parse_search_page, meta = {'impersonate': 'chrome'})
            
    def parse_product_page(self, response):

        current_time = datetime.datetime.now()
        yield{
        'dbq_prd_type': 'MADE-TO-ORDER',
        'website_name': 'http://ebay.com/',
        'competence_date': current_time.isoformat(),
        'merchant_location': response.css('div.ux-labels-values__values.col-9 span.ux-textspans.ux-textspans--SECONDARY::text').getall(),
        'currency_code': 'USD',
        'merchant_name': response.xpath('//*[@id="STORE_INFORMATION"]/div/div/div[1]/div[1]/div[2]/div[2]/h2/a/span/text()').get(),
        'merchant_url': response.xpath('//*[@id="STORE_INFORMATION"]/div/div/div[1]/div[1]/div[2]/div[2]/h2/a/@href').get(),
        'merchant_image': response.css('div.ux-action-avatar__wrapper.ux-action-avatar__scrim img::attr(src)').get(),
        'merchant_descr': response.xpath('//*[@id="STORE_INFORMATION"]/div/div/div[1]/div[1]/div[4]/span[2]/span[1]/span/text()').get(),
        'product_code': response.css('div.ux-layout-section__textual-display.ux-layout-section__textual-display--itemId span.ux-textspans.ux-textspans--BOLD::text').get(),
        'description': response.css('div.x-item-title__infoOverlay_content span::text').get(),
        'product_title': response.css('h1.x-item-title__mainTitle span::text').get(),
        'specifications': response.css('div.ux-layout-section-evo__row span::text').getall(),
        'quantity': response.css('div.x-quantity__availability span::text').get(),
        'category1': response.css('ul span::text')[0].get(),
        'category2': response.css('ul span::text')[1].get(),
        'category3': response.css('ul span::text')[2].get(),
        'full_price': response.css('div.x-price-primary span::text').get(),
        'price': response.css('span.x-price-approx__price span::text').get(),
        'itemurl': response.url,
        'main_image_url':response.css('div.ux-image-carousel.zoom.img-transition-medium img::attr(src)').get(),
        'rendered_img': response.css('div.ux-image-carousel.zoom.img-transition-medium img::attr(src)').getall(),
        'all_images': response.css('button.ux-image-grid-item.image-treatment.rounded-edges img::attr(src)').getall(),
       
         }