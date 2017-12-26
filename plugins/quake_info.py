# -*- coding: utf-8 -*-
import requests
import os
import slackbot_settings
from slacker import Slacker

def main():
    exist_time = ""
    time_file_name = 'time_info.txt'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    headers = { 'User-Agent' : user_agent }
    resp = requests.get('https://api.p2pquake.net/v1/human-readable',headers=headers).json()
    # code 551: 地震情報，552: 津波予報，5610: 集計済み地震感知情報
    for i in range(10):
        if resp[i]['code'] == 551:
            time_info = resp[i]['time']
            if os.path.exists(time_file_name):
                f = open(time_file_name,"r")
                exist_time = f.read()
                f.close()
            if exist_time == "" or exist_time < time_info:
                if os.path.exists(time_file_name):
                    os.remove(time_file_name)
                f = open(time_file_name,"w")
                f.write(time_info)
                f.close()
                message = "***** 地震情報 *****"
                info = resp[i]['earthquake']
                message += "\n発生日時:" + info['time']
                maxScale_info = scale(info['maxScale'])
                message += "\n最大震度:" + maxScale_info
                domesticTsunami_info = domesticTsunami(info['domesticTsunami'])
                message += "\n津波の有無:" + domesticTsunami_info
                info_hypocenter = info['hypocenter']
                if info_hypocenter['name'] != "":
                    message += "\n震源地:" + info_hypocenter['name']
                else:
                    message += "\n震源地:不明"
                message += "\n深さ:" + info_hypocenter['depth']
                if info_hypocenter['magnitude'] != "-1.0":
                    message += "\nマグニチュード:" + info_hypocenter['magnitude']
                else:
                    message += "\nマグニチュード:取得エラー"
                points = resp[i]['points']
                if len(points) != 0:
                    for j in range(len(points)):
                        point_scale = scale(points[j]['scale'])
                        message += "\n場所:" + points[j]['addr'] + "/" + point_scale
                else:
                    message += "\n詳細不明"
                print(message)
                slack = Slacker(slackbot_settings.API_TOKEN)
                slack.chat.post_message('weather', message, as_user=True)

def scale(scale_value):
    scale_info = ""
    # 震度　0(なし)、10(震度1)、20(2)、30(3)、40(4)、45(5弱)、50(5強)、55(6弱)、60(6強)、70(7)
    if scale_value == 0:
        scale_info = "なし"
    if scale_value == 10:
        scale_info = "震度1"
    if scale_value == 20:
        scale_info = "震度2"
    if scale_value == 30:
        scale_info = "震度3"
    if scale_value == 40:
        scale_info = "震度4"
    if scale_value == 45:
        scale_info = "震度5弱"
    if scale_value == 50:
        scale_info = "震度5強"
    if scale_value == 55:
        scale_info = "震度6弱"
    if scale_value == 60:
        scale_info = "震度6強"
    if scale_value == 70:
        scale_info = "震度7"
    if scale_value is None :
        scale_info = "不明"
    
    return(scale_info)

def domesticTsunami(domesticTsunami_value):
    domesticTsunami_info = ""
    # 津波 None(なし)、Unknown(不明)、Checking(調査中)、NonEffective(若干の海面変動[被害の心配なし])、Watch(津波注意報)、Warning(津波予報[種類不明])

    if domesticTsunami_value == "Unknown":
        domesticTsunami_info = "不明"
    if domesticTsunami_value == "Checking":
        domesticTsunami_info = "調査中"
    if domesticTsunami_value == "NonEffective":
        domesticTsunami_info = "若干の海面変動[被害の心配なし]"
    if domesticTsunami_value == "Watch":
        domesticTsunami_info = "津波注意報"
    if domesticTsunami_value == "Warning":
        domesticTsunami_info = "津波予報[種類不明]"
    if domesticTsunami_value == "None":
        domesticTsunami_info = "なし"
    return(domesticTsunami_info)

if __name__ == '__main__':
    main()