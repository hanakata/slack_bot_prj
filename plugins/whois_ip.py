# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 09:59:46 2017

@author: mkatayama
"""
import ipaddress
from ipwhois import IPWhois
from slackbot.bot import respond_to

@respond_to('IP(.*)調べて')
@respond_to('IP(.*)しらべて')
def whois(message, something):
    ip = '{0}'.format(something)
    response_string = ""

    if(ip == "" ):
        response_string = "IPアドレスが抜けています。"
    else:
        try:
            ip_check = ipaddress.ip_address(ip).is_private
            if(ip_check == True):
                response_string = "プライベートアドレスです。\n"
            else:
                obj = IPWhois(ip)
                results = obj.lookup(get_referral=True)

                for result_net in results['nets']:
                    response_string += "cidr:" + result_net["cidr"] + "\n"
                    response_string += "name:" + result_net["name"] + "\n"
                    response_string += "description:" + result_net["description"] + "\n"
                    response_string += "country:" + result_net["country"] + "\n"
                    response_string += "\n"
        except:
            response_string = "検索に失敗しました。\n"

    message.reply(response_string)