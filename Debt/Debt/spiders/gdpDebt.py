# -*- coding: utf-8 -*-
import scrapy


class GdpdebtSpider(scrapy.Spider):
    name = 'gdpDebt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//table/tbody/tr")
        for row in rows:
            name = row.xpath(".//td[1]/a/text()").get()
            link = row.xpath(".//td[1]/a/@href").get()
            debt_to_gdp_per = row.xpath(".//td[2]/text()").get()

            yield  response.follow(url=link,
                                   callback=self.parse_moredata,
                                   meta={'name':name})

    def parse_moredata(self,response):
        rows = response.xpath("//div[@class='sidebar-rows']/div")
        count_name = response.request.meta['name']
        country = dict()
        country['Country'] = count_name
        for row in rows:
            label = row.xpath(".//div[@class='rowlabel']/text()").get()
            if label != None:
                simple = row.xpath(".//div[@class='rowvalue']/text()").get()
                value = row.xpath(".//div[@class='rowvalue']/span/text()").get()
                link = row.xpath(".//div[@class='rowvalue']//a/text()").get()
                valuedouble = row.xpath(".//div[@class='rowvalue']//span/text()").get()
                if simple!=None:
                    country[label] = simple
                elif valuedouble!=None:
                    country[label] = valuedouble
                elif value !=None:
                    country[label] = value
                elif link!=None:
                    country[label] = link
        yield country
    # Use the command scrapy crawl spidername -o dataset_name.extension