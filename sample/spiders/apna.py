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
            company = job.xpath(".//div[@class='JobCardList__Grid-sc-1v9ot9b-1 heAxPY']/div/div/div/p/text()").get()
            salary = job.xpath(".//div[@class='styles__JobSalaryAndType-sc-1eqgvmq-2 juzRZt']/div/text()").get()
            
            

            yield {
                'title': title.strip(),
                'company': company.strip(),
                'salary': salary.strip(),
            }
