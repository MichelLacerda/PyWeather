# -*- coding: utf-8 -*-
import urllib
import json

__author__ = "Michel Lacerda"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"
__copyright__ = "Copyright 2015, Michel Lacerda"
__version__ = "0.4b"

# (Estado, Sigla(uf), 'Capital', WOEID)
capital = [
    ('Acre', 'AC', 'Rio Branco', 455904),
    ('Alagoas', 'AL', 'Maceió', 455880),
    ('Amapá', 'AP', 'Macapá', 455970),
    ('Amazonas', 'AM', 'Manaus', 455833),
    ('Bahia', 'BA', 'Salvador', 455826),
    ('Ceará', 'CE', 'Fortaleza', 455830),
    ('Distrito Federal', 'DF', 'Brasília', 455819),
    ('Espírito Santo', 'ES', 'Vitória', 455922),
    ('Goiás', 'GO', 'Goiânia', 455831),
    ('Maranhão', 'MA', 'São Luís', 455834),
    ('Mato Grosso', 'MT', 'Cuiabá', 455829),
    ('Mato Grosso do Sul', 'MS', 'Campo Grande', 455849),
    ('Minas Gerais', 'MG', 'Belo Horizonte', 455821),
    ('Pará', 'PA', 'Belém', 455820),
    ('Paraíba', 'PB', 'João Pessoa', 455872),
    ('Paraná', 'PR', 'Curitiba', 455822),
    ('Pernambuco', 'PE', 'Recife', 455824),
    ('Piauí', 'PI', 'Teresina', 455835),
    ('Rio de Janeiro', 'RJ', 'Rio de Janeiro', 455825),
    ('Rio Grande do Norte', 'RN', 'Natal', 455888),
    ('Rio Grande do Sul', 'RS', 'Porto Alegre', 455823),
    ('Rondônia', 'RO', 'Porto Velho', 455901),
    ('Roraima', 'RR', 'Boa Vista', 455936),
    ('Santa Catarina', 'SC', 'Florianópolis', 455861),
    ('São Paulo', 'SP', 'São Paulo', 455827),
    ('Sergipe', 'SE', 'Aracaju', 455839),
    ('Tocantins', 'TO', 'Palmas', 457721),
]

capital_default = capital[0]

# CODE, DESCRIPTION en-EN, DESCRIPTION pt-BR
condition = [
    (0, 'tornado', ''),
    (1, 'tropical storm', ''),
    (2, 'hurricane', ''),
    (3, 'severe thunderstorms', ''),
    (4, 'thunderstorms', ''),
    (5, 'mixed rain and snow', ''),
    (6, 'mixed rain and sleet', ''),
    (7, 'mixed snow and sleet', ''),
    (8, 'freezing drizzle', ''),
    (9, 'drizzle', ''),
    (10, 'freezing rain', ''),
    (11, 'showers', ''),
    (12, 'showers', ''),
    (13, 'snow flurries', ''),
    (14, 'light snow showers', ''),
    (15, 'blowing snow', ''),
    (16, 'snow', ''),
    (17, 'hail', ''),
    (18, 'sleet', ''),
    (19, 'dust', ''),
    (20, 'foggy', ''),
    (21, 'haze', ''),
    (22, 'smoky', ''),
    (23, 'blustery', ''),
    (24, 'windy', ''),
    (25, 'cold', ''),
    (26, 'cloudy', ''),
    (27, 'mostly cloudy (night)', ''),
    (28, 'mostly cloudy (day)', ''),
    (29, 'partly cloudy (night)', ''),
    (30, 'partly cloudy (day)', ''),
    (31, 'clear (night)', ''),
    (32, 'sunny', ''),
    (33, 'fair (night)', ''),
    (34, 'fair (day)', ''),
    (35, 'mixed rain and hail', ''),
    (36, 'hot', ''),
    (37, 'isolated thunderstorms', ''),
    (38, 'scattered thunderstorms', ''),
    (39, 'scattered thunderstorms', ''),
    (40, 'scattered showers', ''),
    (41, 'heavy snow', ''),
    (42, 'scattered snow showers', ''),
    (43, 'heavy snow', ''),
    (44, 'partly cloudy', ''),
    (45, 'thundershowers', ''),
    (46, 'snow showers', ''),
    (47, 'isolated thundershowers', ''),
    (3200, 'not available', ''),
]


def search_uf(UF=""):
    filtered =  list(filter(lambda x: x[1] == UF, capital))
    if not filtered:
        return capital_default

    return filtered[0]


def weather(UF=""):
    """Sample Weather API Response

    Keyword arguments:
        uf -- Set acronym of State (default DF)

    Query Example:
        select * from weather.forecast where woeid = 457721 and u='c'

    URL:
        https://query.yahooapis.com/v1/public/yql?

    CONVERT TO JSON:
        &format=json

    Return:
        temp  -- Temperatura atual
        min   -- Temperatura minima
        max   -- Temperatura maxima
        ico   -- Icone
        cond  -- Condicao do tempo
        state -- Estado
        city  -- Cidade
        cod   -- woeid
    """
    UF = UF[-2::].upper()
    uf = search_uf(UF)

    try:
        BASE_URL = "https://query.yahooapis.com/v1/public/yql?"
        QUERY = """select * from weather.forecast where woeid = {0} and u='c'""".format(uf[3])
        URL = "{0}{1}{2}".format(BASE_URL, urllib.urlencode({'q': QUERY}), "&format=json")

        result = urllib.urlopen(URL).read()
        __data = json.loads(result)

        data = __data['query']['results']['channel']['item']
        temp = data['condition']['temp']
        low = data['forecast'][1]['low']
        high = data['forecast'][1]['high']
        icon = data['description'].split('<img src="')[1].split('"/>')[0]

        results = {"temp": temp, "min": low, "max": high, "icon": icon,
                   "state": uf[0], "city": uf[2], "cod": uf[3]}
    except:
        results = {"temp": 0, "min": 0, "max": 0,
                   "icon": u'http://l.yimg.com/a/i/us/we/52/11.gif',
                   "state": 0, "city": 0, "cod": 0}
    return results


print(eather('MG'))
