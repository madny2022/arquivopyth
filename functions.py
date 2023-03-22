import csv
import json
import requests
import logging
import telebot
import pandas as pd
from time import sleep
from datetime import datetime
from notifypy import notify
from pushbullet import Pushbullet


def results():
    data = pd.read_csv('count.csv')
    wins = sum(n for n in data.win)
    losses = sum(n for n in data.loss)
    prim_tent = sum(n for n in data.prim_tent)
    prim_gale = sum(n for n in data.prim_gale)
    seg_gale = sum(n for n in data.seg_gale)
    porcentagem = round((wins - losses) / wins * 100, 2)

    return {'wins': wins, 'losses': losses, 'prim_tent': prim_tent, 'prim_gale': prim_gale, 'seg_gale': seg_gale, 'porcentagem': porcentagem}


def count(time, win:int, loss:int, prim_tent:int, prim_gale:int, seg_gale:int,bot_telegram):
    with open('count.csv', 'a+') as file:
        writer = csv.writer(file)
        writer.writerow([time, win, loss, prim_tent, prim_gale, seg_gale])
        #bot_telegram.send_message('-749878368', [time, win, loss, prim_tent, prim_gale, seg_gale])


# desktop notification settings
def desktop_notification(message):
    notification = Notify()
    notification.title = 'Blaze'
    notification.message = message
    notification.icon = r'C:\Users\User\Downloads\python projects\blaze_bot\blaze-icon.png'
    notification.send()

# phone notifications
def bot_msg(title, message):
    pb = Pushbullet('o.9mKgLukDRUkGzzaWN9DIC0aqy3ixNHKj')
    pb.push_note(title, message)

# basic api request
def roulette_preview():
    global last_doubles
    last_doubles = last_doubles[1:]
    colored_string = ', '.join([
        f"\033[10;40m {item[0]} \033[m" if item[1] == "preto"
        else f"\033[10;41m {item[0]} \033[m" if item[1] == "vermelho"
        else f"\033[10;47m {item[0]} \033[m" for item in last_doubles])
    print(f"\r{colored_string}", end="")


def get_color(number):
    colors = {
        0: "branco",
        1: "vermelho",
        2: "preto"
    }
    return colors.get(number, None)

def request():
    try:
        while True:  
            req = requests.get('https://blaze.com/api/roulette_games/recent', headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            if req.status_code == 200:
                break
        output = json.loads(req.text)
        list_past_results = [{"color": "branco" if i["color"] == 0 else "vermelho" if i["color"] == 1 else "preto",
                     "value": i["roll"]} for i in output]
        return list_past_results
    except: pass

# main function
def main_request(bot_telegram):
    logging.basicConfig(filename='tracker.log',level=logging.DEBUG, format = '%(asctime)s:%(message)s')
    while True:
        
        list_past_results = request()
        # if list_past_results[0]['color'] =='1' and list_past_results[1]['color']=='2' and list_past_results[1]['numero']==14
        #   # estrategia2(list_past_results,bot_telegram)
        # elif            
        if list_past_results[0]['color'] == "vermelho" and list_past_results[1]['color'] == "preto":
            return print('⚫️/🔴 ESTRATEGIA 2📌'),apostar(list_past_results, bot_telegram)

        print('Request feito:', datetime.now())
        sleep(1)

# 

def apostar(lista, bot_telegram):

    #elif
    if lista[0]['color']:
        # desktop_notification('Apostar no vermelho e no branco')
        # bot_msg('Blaze', 'Apostar no vermelho e no branco.')
        while True:
            try:
                bot_telegram.send_message('-749878368', '\U0001f916 Robô da Safablaze \U0001f916 \n\nApostar no vermelho e no branco. \U0001f534 \u26aa')
                break
            except Exception as e:
                print('Erro:', e)
    #elif


    win = 0
    loss = 0
    prim_tent = 0
    prim_gale = 0
    seg_gale = 0


    # checking if you won
    while True:
        new_list = request()
        if lista != new_list:
            list = new_list
            break

    if list[0]['color'] == list[1]['color']:
        prim_tent += 1
        # desktop_notification('WIIINNNN')
        # bot_msg('Blaze','WIIINNN')
        while True:
            try:
                #bot_telegram.send_message('-749878368', 'WIIINNN')
                bot_telegram.send_photo('-749878368', photo=open('Green.png', 'rb'))
                break
            except Exception as e:
                print('Erro:', e)
        win += 1
        print('WIINN')
    else:
        # desktop_notification('Vamos para a primeira gale. \nDobre a aposta e repita a cor')
        # bot_msg('Blaze', 'Vamos para a primeira gale. \nDobre a aposta e repita a cor')
        while True:
            try:
                bot_telegram.send_message('-749878368', '\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f  \nVamos para a primeira gale. \nDobre a aposta e repita a cor')
                
                break
            except Exception as e:
                print('Erro:', e)
        print('Primeira gale')

        sleep(1)
        while True:
            new_list = request()
            if list != new_list:
                list = new_list
                break

        if list[0]['color'] == list[1]['color']:
            prim_gale += 1
            # desktop_notification('WIIINNNN')
            # bot_msg('Blaze', 'WIIINNN')
            while True:
                try:
                    #bot_telegram.send_message('-749878368', '\u2705 \u2705 \u2705 \u2705 \nWIIINNN')
                    bot_telegram.send_photo('-749878368', photo=open('Green.png', 'rb'))
                    break
                except Exception as e:
                    print('Erro:', e)
            win += 1
            print('WINN')
            
        else:
            sleep(1)
            # desktop_notification('Vamos para a segunda gale. \nDobre a aposta e repita a cor.')
            # bot_msg('Blaze', 'Vamos para a segunda gale. \nDobre a aposta e repita a cor.')
            while True:
                try:
                    bot_telegram.send_message('-749878368', '\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \nVamos para a segunda gale. \nDobre a aposta e repita a cor.')
                    break
                except Exception as e:
                    print('Erro:', e)
            print('Segunda gale')

            while True:
                new_list = request()
                if list != new_list:
                    list = new_list
                    break

            if list[0]['color'] == list[1]['color']:
                # desktop_notification('WIIINNNN')
                # bot_msg('Blaze', 'WIIINNN')
                while True:
                    try:
                        #bot_telegram.send_message('-749878368', '\u2705 \u2705 \u2705 \u2705 \nWIIINNN')
                        bot_telegram.send_photo('-749878368', photo=open('Green.png', 'rb'))
                        break
                    except Exception as e:
                        print('Erro:', e)
                seg_gale += 1
                win += 1
                print('WINN')
            else:
                # desktop_notification('Loss')
                # bot_msg('Blaze', 'Loss')
                while True:
                    try:
                        #bot_telegram.send_message('-749878368', '\u274c \u274c \u274c \u274c \nLoss')
                        bot_telegram.send_photo('-749878368', photo=open('Loss.png', 'rb'))
                        break
                    except Exception as e:
                        print('Erro:', e)
                loss += 1
                print('loss')

    sleep(2)
    time = datetime.now()
    count(time, win, loss, prim_tent, prim_gale, seg_gale,bot_telegram)

    while True:
        new_list = request()
        if list != new_list:
            main_request(bot_telegram)



# Cor 2 = Preto | Cor 1 = Vermelho | Cor 0 - Branco