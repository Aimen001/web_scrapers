import scrapy
from booksscraper.items import BookItem


class Booksgrape(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    c_settings={"FEEDS": { "items.json": {"format": "json"}}}

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            product_page = book.css('h3 a').attrib['href']
            if product_page:
                if 'catalogue/' in product_page:
                    product_page_url = 'https://books.toscrape.com/' + product_page
                else:
                    product_page_url = 'https://books.toscrape.com/catalogue/' + product_page
            yield response.follow(product_page_url, callback=self.parse_book_page)

        # Handling next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):

        table_row = response.css('table tr')
        book_item = BookItem()

        book_item['product_name'] = response.xpath('//article/div[1]/div[2]/h1/text()').get()
        book_item['price'] = response.xpath('//article/div[1]/div[2]/p[1]/text()').get()
        book_item['category'] = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get()
        book_item['rating'] = response.css('p.star-rating::attr(class)').get()
        book_item['UPC'] = table_row[0].css('td::text').get()
        book_item['Product_Type'] = table_row[1].css('td::text').get()
        book_item['Price_excl_tax'] = table_row[2].css('td::text').get()
        book_item['Price_incl_tax'] = table_row[3].css('td::text').get()
        book_item['Tax'] = table_row[4].css('td::text').get()
        book_item['Availability'] = table_row[5].css('td::text').get()
        book_item['Number_of_reviews'] = table_row[6].css('td::text').get()
        book_item['Description'] = response.xpath('//meta[@name="description"]/@content').get()
        
        yield book_item