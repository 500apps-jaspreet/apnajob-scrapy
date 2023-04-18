import scrapy

class ApnaSpider(scrapy.Spider):
    name = 'apna'
    allowed_domains = ['https://apna.co/jobs']
    start_urls = ['https://apna.co/jobs']


    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'jobs.json'
    }


    def parse(self, response):
        titles = response.xpath("//div[@class='JobCardList__Grid-sc-1v9ot9b-1 heAxPY']/div/div/div/h3/a/text()").getall()
        # company_name = response.xpath(" //p[@class='styles__JobOrganizationName-sc-1eqgvmq-6 hqjYPR']").getall()


        for title in titles:

        #      yield {'title': title.strip(),'companyname':company_name.strip()}
        #      yield(title, company_name)
            yield {'title': title.strip()}
            yield(title)

        print(response)
        ############################


