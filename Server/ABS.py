#version 0.1.0
#-----------ИМПОРТ МОДУЛЕЙ------------
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config #Импорт config-файла для локализации pyowm
from dotenv import load_dotenv, find_dotenv #Импорт модуля работы с ENV файлами
import os
import time
import datetime
import socket
from error_list import api_error_window

#---Подключение ENV и config файла----
config_dict = get_default_config()
config_dict['language'] = 'ru'
config_dict['metric_system'] = 'metric'
config_dict['speed_unit'] = 'meters_second'
load_dotenv(find_dotenv())

#-------НАСТРОЙКА API И ГОРОДА--------
try:
    owm = OWM(os.getenv('API_KEY'), config_dict) #Получаем API-ключ из ENV-файла
    mgr = owm.weather_manager()
    obser = mgr.weather_at_coords(55.7557, 37.6173) #Указываем координаты города для которого выводится погода
    w = obser.weather
except Exception as e:
    api_error_window(e)

#--------------ФУНКЦИИ----------------
def wind_dir(degrees): #Функция определения направления ветра
    directions = ['северный', 'северовосточный', 'восточный', 'юговосточный', 'южный', 'югозападный', 'западный',
                  'северозападный', 'северный']
    index = round(degrees / 45) % 8
    return directions[index]

def temp_rus(numb): #Функция склонения градусов
    if 10 < numb % 100 < 20:
        return f'{numb} градусов'
    else:
        if numb % 10 == 1:
            return f'{numb} градус'
        elif 2 <= numb % 10 <= 4:
            return f'{numb} градуса'
        else:
            return f'{numb} градусов'

def format_meters(value): #Функция склонения метров
    if value % 10 == 1 and value % 100 != 11:
        return f"{value} метр"
    elif value % 10 == 2 and value % 100 != 12 or value % 10 == 3 and value % 100 != 13 or value % 10 == 4 and value % 100 != 14:
        return f"{value} метра"
    else:
        return f"{value} метров"

def send_udp_message(message): #Функция сервера UDP
    UDP_IP = '192.168.0.106'  # IP-адрес получателя
    UDP_PORT = 1234  # Порт получателя
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    sock.close()

#--------------ОСНОВА-----------------
while True:
#Вывод данных из pyowm
    dstat = w.detailed_status  # 'clouds' (Погода)

    windir = w.wind()  # {'speed': 4.6, 'deg': 330} (Ветер, скорость и направление)
    value_wind_deg = windir['deg']
    dwind_speed = round(float(windir['speed'])) #Округляем скорость ветра до целого числа
    dwind_speed_form = format_meters(dwind_speed) #Функция склонения
    dwind_deg = wind_dir(value_wind_deg) #Функция склонения

    dhum = w.humidity  # 87 (Влажность)

    dtemperature = w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0} (Температура)
    dtemp = round(float(dtemperature['temp'])) #Округляем среднюю температуру до целого числа
    dtemp_rus = temp_rus(dtemp) #Функция склонения

    drain = str(w.rain)  # {} Статус дождя
    rain_status = "" if drain else " Идёт дождь"

    w.clouds  # 75 (Облачность в процентах)

#Вывод времени и даты
    ntime = datetime.datetime.now()
    months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня", 7: "июля", 8: "августа",
              9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}  # Словарь с названиями месяцев в родительном падеже
    nmonth = months[ntime.month]  # Получение названия месяца по номеру

#Погода через 3 часа(В РАЗРАБОТКЕ)

#Финальный вывод
    print(f'Автономная система вещания. Сегодня {ntime.day} {nmonth}. Средняя температура {dtemp_rus} по Цельсию, {dstat}. '
          f'Ветер {dwind_deg}, {dwind_speed_form} в секунду.{rain_status}')
#Отправка по UDP
    message = f'Автономная система вещания. Сегодня {ntime.day} {nmonth}. Средняя температура {dtemp_rus} по Цельсию, {dstat}. Ветер {dwind_deg}, {dwind_speed_form} в секунду.{rain_status}'  # Сообщение для отправки
    send_udp_message(message)
    time.sleep(1800) #Отправляет сообщение по UDP каждые 30 минут


