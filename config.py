import os
import kivy
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex

PATH_SEPERATOR = '\\' if os.path.realpath(__file__).find('\\') != -1 else '/'

PROJECT_PATH = PATH_SEPERATOR.join(os.path.realpath(__file__).\
                                    split(PATH_SEPERATOR)[:-1])

WORK_TIME_PERIOD = 30
BREAK_TIME_PERIOD = 10

KIVY_FONTS = [{
        "name": "WebAwesome",
        "fn_regular": "%(pp)s%(ps)sassets%(ps)sfontawesome-webfont.ttf"%{'pp':PROJECT_PATH,
                                                                         'ps':PATH_SEPERATOR},
    },{
        "name": "FiraSans",
        "fn_regular": "%(pp)s%(ps)sassets%(ps)sFiraSans-Regular.ttf"%{'pp':PROJECT_PATH,
                                                                         'ps':PATH_SEPERATOR},
    }]


for font in KIVY_FONTS:
    LabelBase.register(**font)

KIVY_VERSION = kivy.__version__

KIVY_DEFAULT_FONT = "FiraSans"
KIVY_DEFAULT_FONT_PATH = filter(lambda x: x['name'] == KIVY_DEFAULT_FONT, KIVY_FONTS)[0]['fn_regular']

KIVY_ICONIC_FONT = "WebAwesome"
KIVY_ICONIC_FONT_PATH = filter(lambda x: x['name'] == KIVY_ICONIC_FONT, KIVY_FONTS)[0]['fn_regular']

COLOR1 = get_color_from_hex('E62E25')
COLOR_RED = (1,.85,.85,1)
COLOR_BLUE = (.85,.85,1,1)
