import scrapy

class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?position=1&pageNum=0&start='

    def start_requests(self):
        first_job_on_the_page = 0
        url = self.start_url + str(first_job_on_the_page)
        yield scrapy.Request(url=url, callback=self.parse, meta={'first_job_on_the_page': first_job_on_the_page})

    def parse(self, response):
        first_job_on_the_page = response.meta['first_job_on_the_page']

        jobs = response.css("li")
        num_jobs_returned = len(jobs)
        
        print(f"******* Num Jobs Returned: {num_jobs_returned} *******")

        for job in jobs:
            
            job_title = job.css('h3.base-search-card__title::text').get()
            company_name = job.css('h4.base-search-card__subtitle a::text').get()
            location = job.css('div.base-search-card__metadata span::text').get()
            date_posted = job.css('div.base-search-card__metadata time::attr(datetime)').get()
            time_went = job.css('div.base-search-card__metadata time::text').get()
            job_link = job.css('a.base-card__full-link.absolute::attr(href)').get()
            company_link = job.css('h4.base-search-card__subtitle a::attr(href)').get()

            if job_title and company_name:
                yield {
                    'job_title': job_title.strip() if job_title else '',
                    'company_name': company_name.strip() if company_name else '',
                    'location': location.strip() if location else '',
                    'date_posted': date_posted.strip() if date_posted else '',
                    'time_went': time_went.strip() if time_went else '',
                    'job_link': job_link.strip() if job_link else '',
                    'company_link': company_link.strip() if company_link else '',
                }

        if num_jobs_returned > 0:
            first_job_on_the_page = int(first_job_on_the_page) + 25
            next_url = self.start_url + str(first_job_on_the_page)
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'first_job_on_the_page': first_job_on_the_page})
