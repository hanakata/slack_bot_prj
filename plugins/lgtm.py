# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from slackbot.bot import listen_to,respond_to

@listen_to('lgtm')
def lgtm(message):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        url = 'http://www.lgtm.in/g'
        target_html = requests.get(url,headers=headers)
        html = BeautifulSoup(target_html.text, "lxml")

        lgtm_info_full = html.find('div', class_="thumbnail")

        for lgtm_info in lgtm_info_full:
            lgtm = lgtm_info.find('img')
            if type(lgtm) is not int:
                response_string = lgtm['src']
    except:
        response_string = "検索に失敗しました。\n"

    message.reply(response_string)