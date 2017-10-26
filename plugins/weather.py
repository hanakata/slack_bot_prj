import urllib, sys
import json
from slackbot.bot import respond_to

@respond_to('天気')
def weather(message):
    try: citycode = sys.argv[1]
    except: citycode = '130010'
    resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    response_string = ""
    
    resp = json.loads(resp)
    response_string += '**************************'
    response_string += '\n'+resp['title']
    response_string += '\n**************************'
    response_string += '\n'+resp['description']['text']

    for forecast in resp['forecasts']:
        response_string += '\n**************************'
        response_string += '\n'+forecast['dateLabel']+'('+forecast['date']+')'
        response_string += '\n'+forecast['telop']
        if forecast['temperature']['max'] is None:
            response_string += '\nNone'
        else:
            response_string += '\n'+forecast['temperature']['max']['celsius']

        if forecast['temperature']['min'] is None:
            response_string += '\nNone'
        else:
            response_string += '\n'+forecast['temperature']['min']['celsius']
    response_string += '\n**************************'

    message.reply(response_string)
