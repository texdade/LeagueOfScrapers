import os
import json
import selenium

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#Install driver
opts=webdriver.ChromeOptions()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.headless=True

driver = webdriver.Chrome(options=opts)
'''
#Install driver
opts=webdriver.ChromeOptions()
opts.headless=True

driver = webdriver.Chrome(ChromeDriverManager().install() ,options=opts)
'''
# GET - returns the best three counters with win rate, empty if no stats are available
class FindCounter(Resource):
    def get(self, champion):
        url = "https://www.op.gg/champion/{}/statistics/".format(champion.lower())
        driver.get(url)
        data = {}

        if(driver.page_source != None):
            try:
                counters = driver.find_elements_by_xpath('//td[@class="champion-stats-header-matchup__table__champion"]')
                winrates = driver.find_elements_by_xpath('//td[@class="champion-stats-header-matchup__table__winrate"]')
            except NoSuchElementException:
                return data, 404

            for counter, wr in zip(counters, winrates):
                champ_name = counter.text
                win_rate = wr.text
                if(champ_name != ""):
                    data[champ_name] = {"winRate": win_rate}

            return data, 200
        return data, 404

# GET - returns all the winrates for the selected champion, empty if no stats are available
class WinRates(Resource):
    def get(self, champion):
        url = "https://www.op.gg/champion/{}/statistics/".format(champion.lower())
        driver.get(url)
        data = {}

        if(driver.page_source != None):
            #in order to get the data, get to the "counters" page by clicking the right "button"
            try:
                elem = driver.find_element_by_xpath('//li[@data-tab-show-class="championLayout-matchup"]')
                driver.execute_script("arguments[0].click();", elem)
            except NoSuchElementException:
                return data, 404

            #wait to the page to load after click
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
        return data, 404

# GET - returns all champions and their winrates for a specific role (bot, support, mid, jungle, top)
class Role(Resource):
    def checkRoles(self, position):
        position = position.lower()
        if(position == "top"):
            return "TOP"
        elif(position == "mid" or position == "middle"):
            return "MID"
        elif(position == "jungle" or position == "jungler"):
            return "JUNGLE"
        elif(position == "support"):
            return "SUPPORT"
        elif(position == "adc" or position == "bottom"):
            return "ADC"
        else:
            return -1

    def get(self, role):
        url = "https://www.op.gg/champion/statistics"
        driver.get(url)
        data = {}

        if(driver.page_source != None):
            role = self.checkRoles(role)

            #if the role is not recognized, send 400 Bad request
            if(role == -1):
                return data, 400

            try:
                trs = driver.find_elements_by_xpath('//tbody[@class="tabItem champion-trend-tier-{}"]/tr'.format(role))
            except NoSuchElementException:
                return data, 404

            for champ in trs:
                champ_name = champ.find_element_by_xpath('.//div[@class="champion-index-table__name"]').get_attribute('textContent')
                print(champ_name)
                elements = champ.find_elements_by_xpath('.//td[@class="champion-index-table__cell champion-index-table__cell--value"]')
                print(elements)
                champ_wr = elements[0].get_attribute('textContent')
                print(champ_wr)
                champ_pr = elements[1].get_attribute('textContent')
                print(champ_pr)
                data[champ_name] = {
                    "winrate" : champ_wr,
                    "pickrate" : champ_pr,
                }

            return data, 200
        return data, 404


class Alive(Resource):
    def get(self):
        return {'alive': 'yes'}, 200


api.add_resource(FindCounter, '/counters/<string:champion>')
api.add_resource(WinRates, '/winrates/<string:champion>')
api.add_resource(Role, '/roles/<string:role>')
api.add_resource(Alive, '/')

if __name__ == '__main__':
    app.run(debug=True)
