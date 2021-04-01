import sys
from pprint import pprint
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python E:\WU\WEB\HTTP\APPsearch.py Санкт-Петербург

# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])
print('\n' * 10)

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
pprint(toponym)
# Координаты центра топонима:Москва, ул. Ак. Королева, 12
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = toponym["boundedBy"]["Envelope"]["lowerCorner"].split(' '), toponym["boundedBy"]["Envelope"][
    "upperCorner"].split(' ')
delta = [str(abs(float(delta[0][0]) - float(delta[1][0]))), str(abs(float(delta[0][1]) - float(delta[1][1])))]
print(delta)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join(delta),
    "l": "sat",
    "pt": ",".join([toponym_longitude, toponym_lattitude, 'pm2wtm'])
}
print(map_params["pt"])

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
print(response.url)
Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы