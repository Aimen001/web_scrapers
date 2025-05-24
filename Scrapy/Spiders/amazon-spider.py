import scrapy

class ProductScraper(scrapy.Spider):
    name = "productscraper"
    allowed_domains = ["amazon.com"]
    custom_settings = {"FEEDS": { "items.json": {"format": "json"}}}
    def __init__(self, *args, **kwargs):
        super(ProductScraper, self).__init__(*args, **kwargs)
        self.scraped_urls = set()  # Initialize inside the instance

    def start_requests(self):
        keywords = ["phone"]
        base_urls = ["https://www.amazon.com/s?k="]

        for keyword in keywords:
            for base_url in base_urls:
                url = f"{base_url}{keyword}"
                yield scrapy.Request(url=url, callback=self.parse, meta={"keyword": keyword})

    def parse(self, response):
        """Extract product links and handle pagination."""
        product_links = response.css("a.a-link-normal.s-no-outline::attr(href)").getall()

        for product_url in product_links:
            absolute_url = response.urljoin(product_url)

            # Check if product URL is already scraped
            if absolute_url not in self.scraped_urls:
                self.scraped_urls.add(absolute_url)  # Mark as scraped
                yield response.follow(url=absolute_url, callback=self.product_parser)

        # Handle pagination
        next_page = response.css("li.s-list-item-margin-right-adjustment a::attr(href)").get()
        if next_page:
            absolute_next_page = response.urljoin(next_page)
            if absolute_next_page != response.url:
                yield response.follow(url=absolute_next_page, callback=self.parse)

    def product_parser(self, response):
        if "amazon.com" in response.url:
            yield {
                "product_name": response.css("h1.a-size-large.a-spacing-none span::text").get(), 
                "price": response.css("span.a-price.aok-align-center span.a-offscreen::text").get(default="N/A").replace("$", ""),
                "about_the_product": [text.strip() for text in response.css("li.a-spacing-mini span::text").getall()],
                "rating": response.css("span#acrPopover span.a-size-base.a-color-base::text").get(default="N/A").strip(),
            }

