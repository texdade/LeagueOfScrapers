import os
import requests
import bs4
import json
import selenium

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#Install driver
opts=webdriver.ChromeOptions()
opts.headless=True

driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)

# GET - returns the best three counters with win rate, empty if no stats are available
class FindCounter(Resource):
    def get(self, champion):
        url = "https://www.op.gg/champion/{}/statistics/".format(champion.lower())
        driver.get(url)
        data = {}

        if(driver.page_source != None):
            counters = driver.find_elements_by_xpath('//td[@class="champion-stats-header-matchup__table__champion"]')
            winrates = driver.find_elements_by_xpath('//td[@class="champion-stats-header-matchup__table__winrate"]')

            for counter, wr in zip(counters, winrates):
                champ_name = counter.text
                win_rate = wr.text
                if(champ_name != ""):
                    data[champ_name] = {"winRate": win_rate}

            return data, 200


class WinRates(Resource):
    def get(self, champion):
        url = "https://www.op.gg/champion/{}/statistics/".format(champion.lower())
        driver.get(url)
        data = {}

        if(driver.page_source != None):
            elem = driver.find_element_by_xpath('//li[@data-tab-show-class="championLayout-matchup"]')
            driver.execute_script("arguments[0].click();", elem)
            driver.implicitly_wait(1)
            divs = driver.find_elements_by_xpath('//div[@class="champion-matchup-champion-list"]/div')
            
            for champ in divs:
                champ_name = champ.get_attribute("data-champion-name")
                champ_wr = champ.get_attribute("data-value-winrate")
                champ_matches = champ.get_attribute("data-value-totalplayed")
                data[champ_name] = {
                    "winrate" : champ_wr,
                    "number of matches" : champ_matches,
                }
                
            return data, 200

class Alive(Resource):
    def get(self):
        return {'alive': 'yes'}, 200


api.add_resource(FindCounter, '/counters/<string:champion>')
api.add_resource(WinRates, '/winrates/<string:champion>')
api.add_resource(Alive, '/')

if __name__ == '__main__':
    app.run(debug=True)
