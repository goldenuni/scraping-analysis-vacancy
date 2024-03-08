import math
import scrapy
from typing import Dict, Any


class WorkUASpider(scrapy.Spider):
    name = "work_ua"
    start_urls = ["https://work.ua/jobs-python/"]
    element_per_page = 14

    def parse(
        self, response: scrapy.http.Response, **kwargs: Any
    ) -> scrapy.Request:
        total_elements = int(
            response.css(".flex .mt-8 .text-default::text")
            .get()
            .strip()
            .split()[0]
        )
        page_number = math.ceil(total_elements / self.element_per_page)

        yield from self._parse_page(response)

        for page in range(2, page_number + 1):
            yield scrapy.Request(
                url=f"https://work.ua/jobs-python/?page={page}",
                callback=self._parse_page,
            )

    def _parse_page(self, response: scrapy.http.Response) -> scrapy.Request:
        for href in response.css(
            "#pjax-jobs-list h2.cut-top a::attr(href)"
        ).getall():
            yield scrapy.Request(
                url=response.urljoin(href), callback=self._parse_single_job
            )

    def _parse_single_job(
        self, response: scrapy.http.Response
    ) -> Dict[str, Any]:
        title = response.css("#h1-name::text").get()
        try:
            city = (
                response.xpath('//p[span[@title="Адреса роботи"]]/text()')
                .getall()[1]
                .strip()
                .split(",")[0]
            )
        except IndexError:
            city = (
                response.xpath('//p[span[@title="Місце роботи"]]/text()')
                .getall()[1]
                .strip()
                .split(",")[0]
            )

        skills = response.css(".js-toggle-block span.ellipsis::text").getall()

        return {
            "title": title,
            "city": city,
            "skills": skills,
        }
