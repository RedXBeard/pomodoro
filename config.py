import os
import kivy
from subprocess import Popen, PIPE
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore


def run_syscall(cmd):
    """
    run_syscall; handle sys calls this function used as shortcut.

    ::cmd: String, shell command is expected.
    """
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.rstrip()

PATH_SEPERATOR = '\\' if os.path.realpath(__file__).find('\\') != -1 else '/'

PROJECT_PATH = PATH_SEPERATOR.join(os.path.realpath(__file__).
                                   split(PATH_SEPERATOR)[:-1])

ICON_PATH = os.path.join(PROJECT_PATH, 'assets/tomato.ico')

WINDOW_SIZE_1 = (200, 240)
WINDOW_SIZE_2 = (300, 150)

STYLE1 = "assets/pomodoro_style1.kv"
STYLE2 = "assets/pomodoro_style2.kv"

ACTIVE_STYLE = "style2"

if PATH_SEPERATOR == '/':
    cmd = "echo $HOME"
else:
    cmd = "echo %USERPROFILE%"

out = run_syscall(cmd)
DATAFILE = "%(out)s%(ps)s.kivypomomdoro%(ps)spomodoro" % {'out': out.rstrip(),
                                                          'ps': PATH_SEPERATOR}
DB = JsonStore(DATAFILE)
directory = os.path.dirname(DATAFILE)
if not os.path.exists(directory):
    os.makedirs(directory)


WORK_TIME_PERIOD = 10
BREAK_TIME_PERIOD = 5

KIVY_FONTS = [{
    "name": "WebAwesome",
    "fn_regular": "%(pp)s%(ps)sassets%(ps)sfontawesome-webfont.ttf" % {'pp': PROJECT_PATH,
                                                                       'ps': PATH_SEPERATOR},
}, {
    "name": "FiraSansRegular",
    "fn_regular": "%(pp)s%(ps)sassets%(ps)sFiraSans-Regular.ttf" % {'pp': PROJECT_PATH,
                                                                    'ps': PATH_SEPERATOR},
}, {
    "name": "FiraSansBook",
    "fn_regular": "%(pp)s%(ps)sassets%(ps)sFiraSans-Book.ttf" % {'pp': PROJECT_PATH,
                                                                 'ps': PATH_SEPERATOR},
}, {
    "name": "FiraSansExtraLight",
    "fn_regular": "%(pp)s%(ps)sassets%(ps)sFiraSans-ExtraLight.ttf" % {'pp': PROJECT_PATH,
                                                                       'ps': PATH_SEPERATOR},
}]


for font in KIVY_FONTS:
    LabelBase.register(**font)

KIVY_VERSION = kivy.__version__

KIVY_DEFAULT_FONT = "FiraSansRegular"
KIVY_DEFAULT_FONT_PATH = filter(
    lambda x: x['name'] == KIVY_DEFAULT_FONT, KIVY_FONTS)[0]['fn_regular']

KIVY_DEFAULT_BOOK_FONT = "FiraSansBook"
KIVY_DEFAULT_BOOK_FONT_PATH = filter(
    lambda x: x['name'] == KIVY_DEFAULT_FONT, KIVY_FONTS)[0]['fn_regular']

KIVY_DEFAULT_EXTRALIGHT_FONT = "FiraSansExtraLight"
KIVY_DEFAULT_EXTRALIGHT_FONT_PATH = filter(
    lambda x: x['name'] == KIVY_DEFAULT_FONT, KIVY_FONTS)[0]['fn_regular']

KIVY_ICONIC_FONT = "WebAwesome"
KIVY_ICONIC_FONT_PATH = filter(
    lambda x: x['name'] == KIVY_ICONIC_FONT, KIVY_FONTS)[0]['fn_regular']

COLOR1 = get_color_from_hex('E62E25')
COLOR_RED = (1, .85, .85, 1)
COLOR_GREEN = get_color_from_hex('52F041')
