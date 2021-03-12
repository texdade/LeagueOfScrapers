import os
import requests
import bs4
import json

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# GET - returns the best three counters with win rate, empty if no stats are available
class FindCounter(Resource):
    def get(self, champion):
        url = "https://www.op.gg/champion/{}/statistics/".format(champion.lower())
        r = requests.get(url)
        data = {}

        if(r.status_code == 200):
            #set up soup for webscraping
            websiteSoup = bs4.BeautifulSoup(r.text, features="html.parser")

            #return
            counters = websiteSoup.find('table', class_='champion-stats-header-matchup__table champion-stats-header-matchup__table--strong tabItem')
            if(counters==None):
                return json.dumps(data), 200

            counters = counters.tbody.find_all("tr")
            #this usually happens when the champion name is typed incorrectly 
            if(counters == []):
                return json.dumps(data), 200
                
            for counter in counters:
                champ_name = "".join([elem for elem in counter.find_all("td")[0].contents if type(elem)==bs4.element.NavigableString])
                
                #champion name appears with a lot of escape characters
                champ_name = "".join([val for val in champ_name if val.isalpha()]) 
                win_rate = counter.find_all("td")[1].b.string

                data[champ_name] = win_rate
            
            return data, 200

class Alive(Resource):
    def get(self):
        return {'alive': 'yes'}, 200

api.add_resource(FindCounter, '/counters/<string:champion>')
api.add_resource(Alive, '/')

if __name__ == '__main__':
    app.run(debug=True)