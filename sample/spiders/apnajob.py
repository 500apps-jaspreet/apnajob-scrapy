import scrapy
from scrapy import Selector


class ApnajobsSpider(scrapy.Spider):
    # Set spider name, allowed domains, and start URLs
    name = "apnajobs"
    allowed_domains = ["apna.co"]
    start_urls = ["https://apna.co/jobs"]
    page_count = 0

    # Main parsing function
    def parse(self, response):
        # Extract job links from the page
        job_links = response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a")
        for job in job_links:
            # Follow job links and parse job details
            job_url = "https://apna.co" + job.xpath('@href').get()
            yield scrapy.Request(url=job_url, callback=self.parse_job)
        self.page_count += 1
        if self.page_count >= 10:
            return
        # Extract URL for next page, if available
        next_page_url = response.css("li:nth-child(7) button:nth-child(1)").get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    # Parse individual job pages
    def parse_job(self, response):
        # Extract job details from the page
        Jobtitle = response.xpath("//h1/text()").get().strip()
        Jobcompany = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()")
        JobArea = response.xpath("//div[contains(@class,'styles__TextJobArea-sc-15yd6lj-7 cHFGaJ')]/text()")
        JobSalary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()").get().strip().replace("\n", "").replace("\t", "")
        try:
            Jobdescription = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get().strip()
        except AttributeError:
            Jobdescription = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get()

        # Create dictionary to store job details
        job_dict = {
            'Jobtitle': Jobtitle,
            'Jobcompany': Jobcompany.get().strip() if Jobcompany else '',
            'JobArea': JobArea.get().strip() if JobArea else '',
            'JobSalary': JobSalary,
            'Jobdescription': Jobdescription
        }
        
        # Extract additional job details from the page
        job_details = response.xpath("//div[@class='styles__JobDetailSection-sc-1532ppx-12 eVTLMf']/div")
        for i in job_details:
            tit = Selector(text=i.get())
            k = tit.xpath("//div[@class='styles__JobDetailBlockHeading-sc-1532ppx-2 iGzafA']/text()")
            v = tit.xpath("//div[@class='styles__JobDetailBlockValue-sc-1532ppx-3 jtaqAv']/text()")
            job_dict[k.get().strip()] = v.get().strip() if v else ''

        # Yield job dictionary
        yield job_dict
