# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import time


class EntitiesSpider(scrapy.Spider):
    name = 'entities'
    allowed_domains = ['arc-sos.state.al.us/cgi/corpmonth.mbr/input']
    start_urls = ['http://arc-sos.state.al.us/cgi/corpmonth.mbr/input']

    def parse(self, response):
        #"http://arc-sos.state.al.us/cgi/corpmonth.mbr/output"
        yield FormRequest.from_response(response, formdata={'month': '1', 'year': '2006', 'place': 'ALL'}, dont_filter=True, callback=self.parse_table)

    def parse_table(self, response):
        print("In Parse_table")
        rows = response.xpath('//table/tr')[1:24]
        for row in rows:
            #time.sleep(2)
            url = row.xpath('.//a/@href')[0].extract()
            absolute_url = response.url.split('/cgi')[0] + url
            #time.sleep(0.8)
            yield Request(absolute_url, dont_filter=True, callback=self.parse_entity)

        next_page = response.xpath('//a[@class="aiSosPageLinks"][contains(text(), "Next")]/@href').extract_first()
        if (next_page):
            print("\nWe're here\n")
            url = response.url.split('mbr/')[0]
            print(url)
            url = url+'mbr/'+next_page
            print(url)
            time.sleep(1)
            yield Request(url, dont_filter=True, callback=self.parse_table)


    def parse_entity(self, response):
        id_number = response.xpath('//td[contains(text(), "Entity ID Number")]//following-sibling::td//text()').extract_first()
        type = response.xpath('//td[contains(text(), "Entity Type")]//following-sibling::td//text()').extract_first()
        principal_address = response.xpath('//td[contains(text(), "Principal Address")]//following-sibling::td//text()').extract_first()
        principal_mailing_address = response.xpath('//td[contains(text(), "Principal Mailing Address")]//following-sibling::td//text()').extract_first()
        status = response.xpath('//td[contains(text(), "Status")]//following-sibling::td//text()').extract_first()
        place_of_formation = response.xpath('//td[contains(text(), "Place of Formation")]//following-sibling::td//text()').extract_first()
        formation_date = response.xpath('//td[contains(text(), "Formation Date")]//following-sibling::td//text()').extract_first()
        reg_agent_name = response.xpath('//td[contains(text(), "Registered Agent Name")]//following-sibling::td//text()').extract_first()
        reg_agent_street = response.xpath('//td[contains(text(), "Registered Office Street")]//following-sibling::td//text()').extract_first()
        reg_agent_mail = response.xpath('//td[contains(text(), "Registered Office Mail")]//following-sibling::td//text()').extract_first()

        incorporators, incorporators_street_address, incorporators_mail_address, members, members_street_address, members_mailing_address = [], [], [], [], [], []

        head = response.xpath('//thead')[1]
        incorporators = head.xpath('.//following::td[contains(text(), "Incorporator Name")]//following-sibling::td/text()').extract()
        incorporators_street_address = head.xpath('.//following::td[contains(text(), "Incorporator Street Address")]//following-sibling::td/text()').extract()
        incorporators_mail_address = head.xpath('.//following::td[contains(text(), "Incorporator Mail Address")]//following-sibling::td/text()').extract()

        members = head.xpath('.//following::td[contains(text(), "Member Name")]//following-sibling::td/text()').extract()
        members_street_address = head.xpath('.//following::td[contains(text(), "Member Street")]//following-sibling::td/text()').extract()
        members_mailing_address = head.xpath('.//following::td[contains(text(), "Member Mail")]//following-sibling::td/text()').extract()


        yield {
            'ID Number': id_number,
            'Type': type,
            'Principal Address': principal_address,
            'Principal Mailing Address': principal_mailing_address,
            'Status': status,
            'Place Of Formation': place_of_formation,
            'Formation Date': formation_date,
            'Registered Agent Name': reg_agent_name,
            'Registered Agent Street Address': reg_agent_street,
            'Registered Agent Mailing Address': reg_agent_mail,
            'Incorporators': incorporators,
            'Incorporators Street Address': incorporators_street_address,
            'Incorporators Mailing Address': incorporators_mail_address,
            'Members': members,
            'Members Street Address': members_street_address,
            'Members Mailing Address': members_mailing_address
        }