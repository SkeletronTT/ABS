# ABS
 Autonomous Broadcasting Station - проект автономной станции вещания погоды и различных сообщений.
# О проекте
Я хочу сделать полностью автономную станцию, однако от автономности одно слово. На данный момент схема работы такова: python-код получает погоду через библиотеку PyOWM, отправляет по WiFi по протоколу UDP на ESP32. Плата преобразует погоду в сигнал и отправляет его по округе на частоте 433 МГц.  
Проект будет состоять из трёх частей: сервер, предатчик и приёмник.  
Сервером будет связка python-файлов, которые получают погоду и отправляют по UDP на ESP32(передатчик). Приёмником будет Arduino nano.
# Необходимые библиотеки
PyOWM - Python оболочка для веб-API OpenWeatherMap  
Python-dotenv считывает пары ключ-значение из файла .env и может устанавливать их в качестве переменных окружения.
```
pip install pyowm python-dotenv
```
# Дисклеймер 
В проекте есть файл `error_list.py` который вызывается при ошибке с API. И ради прикола, я изменил текст ошибки. Пожалуйста, примите во внимание, что текст содержит намеренные ошибки и может быть воспринят как неграмотный. Но воспринимайте это с юмором! Кто сказал, что программирование не может быть веселым?
"Ошибка 404: Хороший юмор не найден"
# Список целей
- [X] Написать серверную часть
- [ ] Сделать исполняемый файл серверной части
- [X] Написать код для передатчика(ESP32) => ТЕСТИРИУЕТСЯ
- [ ] Написать код для приёмника(Arduino Nano)
- [ ] Собрать передатчик
- [ ] Собрать приёмник
- [ ] Сделать систему полностью автономной
# Что нового?
- Версия 0.1.0  
    - Добавлена серверная часть  
    Эту версию можно (и нужно) считать сырой преальфой. Настраивать координаты города надо внутри ABS.py  
    ```python
    obser = mgr.weather_at_coords(55.7557, 37.6173) #Указываем координаты города для которого выводится погода
    ```  
    и env файл необходимо создавать вручную в папке с ABS.py, в котором указан API-ключ.  
    ```
    API_KEY="Ваш API-Ключ"
    ```  
    К примеру:  
    ```
    API_KEY=a1b2.............012g34
    ``` 
    
