import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazonproducts'
    def start_requests(self):
        start_urls = ['https://www.amazon.it/s?k=coccinelle&i=fashion&rh=n%3A5512286031%2Cp_123%3A338700&dc&language=en&ds=v1%3AsCAVb4%2B9A7VfOkYBt4fnawmCrOMHxnZaTZKp1jCa0QY&refresh=2']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search, meta={'impersonate':'chrome'})
    
    def parse_search(self,response):
        headers= response.headers
        products_lists = response.css('div[data-component-type="s-search-result"]')

        for product_list in products_lists:
            product_link = 'https://www.amazon.it' + str(product_list.css('a.a-link-normal.s-no-outline::attr(href)').get())
            yield scrapy.Request(url=product_link,callback=self.parse_product_page,meta={'impersonate':'chrome'})


        next_page = 'https://www.amazon.it' + str(response.css('a.s-pagination-item.s-pagination-next::attr(href)').get())
        if next_page is not None:
            yield scrapy.Request(url=next_page,callback=self.parse_search,meta={'impersonate':'chrome'})

    def parse_product_page(self,response):

        contract_id = 'recUT8OVhNHl4VlNp'
        seller_id = 'AKIAS3CAQLRAAKX7NXNY'
        dbq_prd_type = 'MADE-TO-ORDER'
        website_name = 'https://www.amazon.it'
        competence_date = '2025-04-05'
        country_code = 'ITA'
        currency_code = 'USD'
        merchant_id = response.css('a#sellerProfileTriggerId::attr(href)').get()
        merchant_name = response.css('a#sellerProfileTriggerId::text').get()
        merchant_url = 'https://www.amazon.it' + str(response.css('a#sellerProfileTriggerId::attr(href)').get())
        additional_code_1 = response.xpath('//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[2]/text()').get()
        additional_code_1_type = 'ASIN'
        brand = response.css('div#bylineInfo_feature_div a.a-link-normal::text').get()
        color_info = response.css('div.a-section.a-spacing-none.swatch-image-container img::attr(alt)').getall()
        description = response.css('div#productDescription span::text').getall()
        product_title = response.css('span#productTitle::text').get()
        specifications = response.css('ul.a-unordered-list.a-vertical.a-spacing-small span::text').get()
        delivery = response.css('div#mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE span.a-text-bold::text').get()
        quantity = response.css('select#quantity option::text').getall()
        category1 = response.css('div#wayfinding-breadcrumbs_feature_div a.a-link-normal.a-color-tertiary::text').getall()
        full_price = response.css('div#corePrice_feature_div span.a-offscreen::text').get()
        price = response.css('div#corePrice_feature_div span.a-offscreen::text').get()
        itemurl = response.url
        main_image_url = response.css('span[data-action="main-image-click"] img::attr(src)').get().strip()
        all_images = response.css('span.a-button-text img::attr(src)').getall()

        yield{
                    'contract_id' : contract_id,
                    'seller_id' : seller_id,
                    'dbq_prd_type' : dbq_prd_type,
                    'website_name' : website_name,
                    'competence_date': competence_date,
                    'country_code': country_code,
                    'currency_code': currency_code,
                    'merchant_id': merchant_id,
                    'merchant_name' : merchant_name,
                    'merchant_url' : merchant_url,
                    'additional_code_1': additional_code_1,
                    'additional_code_1_type': additional_code_1_type,
                    'brand' : brand,
                    'color_info' : color_info,
                    'description' : description,
                    'product_title': product_title,
                    'specifications' : specifications,
                    'delivery' : delivery,
                    'quantity' :  quantity,
                    'category1' : category1,
                    'full_price': full_price,
                    'price': price,
                    'itemurl' : itemurl,
                    'main_image_url': main_image_url,
                    'all_images':  all_images,
                }