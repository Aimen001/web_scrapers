import scrapy
import json

class NikeProducts(scrapy.Spider):
    name = 'nikeproducts'

    def start_requests(self):
        start_urls = [
            'https://api.nike.com/discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647?path=/w&searchTerms=jordan&queryType=PRODUCTS&anchor=0&count=24'
        ]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "nike-api-caller-id": "<specific_caller_id>",
            "anonymousId": "<generated_anonymous_id>",
            "cms-auth-token": "<if_required>"
        }
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        data = json.loads(response.text)

        # Check if 'productGroupings' exists
        if 'productGroupings' not in data:
            self.logger.error("Missing 'productGroupings' key in response")
            return

        for grouping in data['productGroupings']:  # Iterate over product groups
            if 'products' not in grouping:
                continue  # Skip if no products

            for product in grouping['products']:
                yield {
                    'groupkey': product.get('groupKey', ''),
                    'productcode': product.get('productCode', ''),
                    'producttype': product.get('productType', ''),
                    'productsubtype': product.get('productSubType', ''),
                    'globalproductid': product.get('globalProductId', ''),
                    'internalPid': product.get('internalPid', ''),
                    'merchProductId': product.get('merchProductId', ''),
                    'title': product.get('copy', {}).get('title', ''),
                    'subtitle': product.get('copy', {}).get('subTitle', ''),
                    'color': product.get('displayColors', {}).get('colorDescription', ''),
                    'current_price': product.get('prices', {}).get('currentPrice', ''),
                    'employeeprice': product.get('prices', {}).get('employeePrice', ''),
                    'initial_price': product.get('prices', {}).get('initialPrice', ''),
                    'image_url': product.get('colorwayImages', {}).get('portraitURL', ''),
                    'url': product.get('pdpUrl', {}).get('url', ''),
                }

        # Handle Pagination
        if 'pages' in data and 'next' in data['pages']:
            next_page = data['pages']['next']
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse, headers=response.request.headers)
