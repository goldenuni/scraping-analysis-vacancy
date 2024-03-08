from pathlib import Path

import scrapy


class WorkUASpider(scrapy.Spider):
    name = "work_ua"
    start_urls = ["https://work.ua/jobs-python/"]

    def parse(self, response):
        for href in response.css("#pjax-jobs-list h2.cut-top a::attr(href)").getall():
            yield scrapy.Request(
                url=response.urljoin(href), callback=self._parse_single_job
            )

    def _parse_single_job(self, response):
        title = response.css("#h1-name::text").get()
        skills = response.css(".js-toggle-block span.ellipsis::text").getall()

        return {
            "title": title,
            "skills": skills,
        }