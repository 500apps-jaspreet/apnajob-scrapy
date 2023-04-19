import scrapy

class ApnaSpider(scrapy.Spider):
    name = 'apna'
    allowed_domains = ['apna.co']
    start_urls = ['https://apna.co/jobs']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'jobs.json'
    }

    def parse(self, response):
        jobs = response.xpath("//div[@class='JobCardList__Grid-sc-1v9ot9b-1 heAxPY']/div")
        for job in jobs:
            title = job.xpath(".//div[@class='JobCardList__Grid-sc-1v9ot9b-1 heAxPY']/div/div/div/h3/a/text()").get()
            location = job.xpath(".//div[@class='JobCard__JobDescription-sc-1j63e6z-1 bzkSml']/p[1]/text()").get()
            company = job.xpath(".//span[contains(@class, 'styles__JobOrganizationName')]/text()").get()
            salary = job.xpath(".//p[contains(text(), '₹')]/text()").get()

            yield {
                'title': title.strip(),
                'location': location.strip(),
                'company': company.strip(),
                'salary': salary.strip(),
            }
