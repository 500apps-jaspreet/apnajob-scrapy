import scrapy
from scrapy import Selector


class ApnaJobsSpider(scrapy.Spider):
    name = "apna_jobs"
    allowed_domains = ["apna.co"]
    start_urls = ["https://apna.co/jobs"]
    page_count = 0

    # Parse the start URL to extract job links
    def parse(self, response):
        # Extract job links from the response
        job_links = response.xpath("//div[@class='styles__JobDetails-sc-1eqgvmq-1 koxkvV']/h3/a")
        
        # Follow each job link and call parse_job to extract job details
        for job_link in job_links:
            job_url = "https://apna.co" + job_link.xpath('@href').get()
            yield response.follow(job_url, callback=self.parse_job)
        
        # Increment the page count and stop parsing after 15 pages
        self.page_count += 1
        if self.page_count >= 15:
            return
        
        # Extract URL for next page, if available, and follow it
        next_page_url = response.css("li:nth-child(7) button:nth-child(1)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    # Parse the job page to extract job details
    def parse_job(self, response):
        # Extract job title, company, area, salary, and description from the response
        job_title = response.xpath("//h1/text()").get(default='').strip()
        job_company = response.xpath("//div[@class='styles__TextJobCompany-sc-15yd6lj-5 kIILUO']/text()")
        job_area = response.xpath("//div[contains(@class,'styles__TextJobArea-sc-15yd6lj-7 cHFGaJ')]/text()")
        job_salary = response.xpath("//div[contains(@class,'styles__TextJobSalary-sc-15yd6lj-8 dGHiHv')]/text()")
        job_salary = job_salary.get(default='').strip().replace("\n", "").replace("\t", "")
        job_description = response.xpath("//div[contains(@class,'styles__JobDescriptionContainer-sc-1532ppx-17 eSHFNy')]/text()").get(default='').strip()

        # Create a dictionary with job details
        job_dict = {
            'job_title': job_title,
            'job_company': job_company.get(default='').strip() if job_company else '',
            'job_area': job_area.get(default='').strip() if job_area else '',
            'job_salary': job_salary,
            'job_description': job_description
        }

        # Extract additional job details from the response
        job_details = response.xpath("//div[@class='styles__JobDetailSection-sc-1532ppx-12 eVTLMf']/div")
        for detail in job_details:
            detail_selector = Selector(text=detail.get())
            key = detail_selector.xpath("//div[@class='styles__JobDetailBlockHeading-sc-1532ppx-2 iGzafA']/text()")
            value = detail_selector.xpath("//div[@class='styles__JobDetailBlockValue-sc-1532ppx-3 jtaqAv']/text()")
            job_dict[key.get(default='').strip().lower().replace(" ", "_")] = value.get(default='').strip() if value else ''

        # Yield the job dictionary
        yield job_dict
