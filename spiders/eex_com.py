# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from datetime import datetime, timedelta

class EexComSpider(scrapy.Spider):
    name = 'eex'
    allowed_domains = ['eex.com']

    column_types = [
        "bestBidPrice",
        "bestAskPrice",
        "noOfTradedContractsExchange",
        "lastTradePrice",
        "lastTradeDifference",
        "lastTradeVolume",
        "volumeExchange",
        "volumeOtc",
        "openInterestNoOfContracts",
    ]

    time_period_future_types = {
        "Year" : { "Base": "P-Power-F-DEAT-Base-Year", "Peak": "P-Power-F-DEAT-Peak-Year" },
        "Quarter": { "Base": "P-Power-F-DEAT-Base-Quarter", "Peak": "P-Power-F-DEAT-Peak-Quarter" },
        "Month": { "Base": "P-Power-F-DEAT-Base-Month", "Peak": "P-Power-F-DEAT-Peak-Month" },
        "Day": { "Base": "P-Power-F-DEAT-Base-Day", "Peak": "P-Power-F-DEAT-Peak-Day" },
    }


    def start_requests(self):
        print "In start_requests..."

        today = datetime.today()

        # single_date.strftime("%d%m-%y")
        todays_date_url = '%d/%d.%d' %(today.year, today.month, today.day)
        today.strftime("%Y/%m.%d")
        url = 'https://www.eex.com/data//view/data/detail/phelix-power-futures/%s%s' %(today.strftime("%Y/%m.%d"), '.json')

        yield scrapy.Request(url, self.parse)


    def parse(self, response):

        print "In parse..."

        response_json = json.loads(response.body)
        data = response_json['data']

        today = datetime.utcnow()

        for time_period, time_period_values in self.time_period_future_types.items():
            print "Time Period: %s; %s" %(time_period, time_period_values)
            for item, item_value in time_period_values.items():
                print "...Time Period item: %s; %s" %(item, item_value)

                phelix_future_time_type_values = (item for item in data if item['identifier'] == item_value).next()
                rows = phelix_future_time_type_values['rows']

                for row in rows:
                    print "......Row: %s" %row['contractIdentifier']
                    for col in self.column_types:
                        print ".........Col: %s" %col

                        series = "eex/phelix/1.0/" + row['contractIdentifier'] + "/" + col
                        # dateTime = today.date()
                        dateTime = self.get_series_date(today.date())
                        if (col in row['data']):
                            value = row['data'][col]

                            yield { 'series': series, 'value': value, 'dateTime': dateTime }


    def get_series_date(self, date):
        year = date.year
        month = date.month
        day = date.day

        return "%d-%d-%d" %(year, month, day)

