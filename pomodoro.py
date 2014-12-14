from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.uix.screenmanager import SlideTransition
from time import strftime, gmtime
from kivy.uix.scatter import Scatter
from datetime import datetime
from config import *

def get_buttons(obj, buttons=[]):
    """
    Buttons which are capable of hover action will
    taken from the root object. Capability is kept
    with buttons extra attribute called 'has_hover'
    """
    for ch in obj.children:
        if hasattr(ch, 'has_hover'):
            buttons.append(ch)
        get_buttons(ch, buttons)
    return buttons

class MyScatterLayout(ScatterLayout):
    rstop = BooleanProperty(False)
    lstop = BooleanProperty(False)
    pre_posx = NumericProperty()
    grab_posx = NumericProperty()

    def on_touch_move(self, touch):
        if 0 <= self.grab_posx + (touch.pos[0] - self.pre_posx) <= 160:
            super(MyScatterLayout, self).on_touch_move(touch)

    def on_touch_down(self, touch):
        super(MyScatterLayout, self).on_touch_down(touch)
        self.pre_posx = touch.pos[0]
        self.grab_posx = self.pos[0]

class Pomodoro(BoxLayout):
    time_period = NumericProperty()
    time_display = StringProperty()
    time_minute = StringProperty()
    time_second = StringProperty()
    rotation = NumericProperty(0)
    sprint_count = NumericProperty(0)
    state = StringProperty()
    start = StringProperty()
    stop = StringProperty()
    buttons = ListProperty()
    count_start = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(Pomodoro, self).__init__(*args, **kwargs)
        self.buttons = get_buttons(self, [])
        self.set_to_workstate()
        self.animation = None
        self.clock = SoundLoader.load('assets/clock.wav')
        self.alarm = SoundLoader.load('assets/alarm.wav')
        if ACTIVE_STYLE == "style1":
            self.sm.current = 'start'

    def start_animation(self):
        """
        starts animation for rotation, if state is on 'work'
        then start date should be taken to log pomodoro.
        other then stop date must be reset in each starting animation action.
        """
        if self.state == "work":
            self.count_start = True
            self.start = str(datetime.now()).rsplit('.', 1)[0]

        elif self.state == "paused" and ACTIVE_STYLE == "style2":
            self.pause_but.disabled = False
            self.state = "work"
            self.count_start = True

        self.stop = ""
        Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)
        if ACTIVE_STYLE == "style1":
            self.start_button.disabled = True
        if ACTIVE_STYLE == "style2":
            self.play_but.disabled = True

    def decrease_minutes(self):
        """
        until the rotation count reaches the end
        minutes and rotation should be continue.
        At the end pomodoro stop date must be taken too
        sounds should also be handled.
        """
        if not self.count_start:
            pass
        elif self.time_period < 1:
            self.rotation = 0
            self.reset_time()
        else:
            self.clock.stop()
            self.clock.play()

            self.rotation += self.perrotation
            self.time_period -= 1
            self.time_display = strftime('%M:%S', gmtime(self.time_period))
            self.time_minute, self.time_second = self.time_display.split(':')

            if ACTIVE_STYLE == "style1":
                if self.animation:
                    self.animation.stop(self)
                self.animation = Animation(rotation=self.rotation, d=1)
                self.animation.start(self)

            if self.state == "work" and self.time_period < 1:
                self.stop = str(datetime.now()).rsplit('.', 1)[0]

            Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)

    def pause_animation(self):
        self.count_start = False
        self.clock.stop()
        self.alarm.stop()
        self.state = 'paused'
        buttons = [self.play_but,
                           self.stop_but,
                           self.pause_but]
        for but in buttons:
            but.disabled = False
        self.pause_but.disabled = True

    def stop_animation(self):
        self.count_start = False
        self.clock.stop()
        self.alarm.stop()
        self.set_to_workstate()
        buttons = [self.play_but,
                           self.stop_but,
                           self.pause_but]
        for but in buttons:
            but.disabled = False

    def switch_screen(self, screen):
        """
        action screens rotation handling
        """
        direction = 'up'
        if ACTIVE_STYLE == "style2" and self.sm.current == self.sm.settings_screen.name:
            direction = 'down'
        self.sm.transition = SlideTransition(direction=direction)
        self.sm.current = screen

    def set_clock(self):
        """
        rotation for per second calculation.
        """
        self.perrotation = Vector(1, 1).angle(
            Vector(1, 1).rotate(360 / float(self.time_period)))

    def set_to_workstate(self):
        """
        the state of pomodoro taken to 'work' time periods and
        required settings handled. for per work pomodoro
        counter counts this state until break state triggered
        """
        self.state = "work"
        self.time_period = WORK_TIME_PERIOD
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.time_minute, self.time_second = self.time_display.split(':')
        self.sprint_count += 1
        self.set_clock()
        if ACTIVE_STYLE == "style1":
            self.switch_screen('start')

    def set_to_breakstate(self):
        """
        Break pomodoro action handled, the time calculated by
        the work state counter then it resets
        """
        self.state = "break"
        self.time_period = BREAK_TIME_PERIOD * self.sprint_count
        self.sprint_count = 0
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.time_minute, self.time_second = self.time_display.split(':')
        self.set_clock()
        if ACTIVE_STYLE == "style1":
            self.switch_screen('start')

    def reset_time(self):
        """
        triggered when the timer reaches the end, animation, clock sound,
        disability of button switched to other state of each.
        pomodoro state changes according to the current one.
        If the current state is 'break' then 'work' state trigger triggered
        """
        if self.animation:
            self.animation.stop(self)
        self.rotation = 0
        self.clock.stop()
        self.alarm.play()
        if ACTIVE_STYLE == "style1":
            self.start_button.disabled = False
        elif ACTIVE_STYLE == "style2":
            buttons = [self.play_but,
                               self.stop_but,
                               self.pause_but]
            for but in buttons:
                but.disabled = False
            if self.state == "work":
                self.state = "break"
                self.set_to_breakstate()
                self.start_animation()
            elif self.state == "break":
                self.set_to_workstate()
        if ACTIVE_STYLE == "style1":
            if self.state == "break":
                self.switch_screen('start')
                self.set_to_workstate()
            else:
                self.switch_screen('info')

    def set_volume(self, state):
        """
        Volume operation handled except alarm sound.
        """
        on_off = 0 if state == "down" else 1
        if self.clock:
            self.clock.volume = on_off

    def keep_info(self, text):
        """
        after each pomodoro in 'work' state an information is taken
        from user and to log that with other necessary informations
        collection is written in a file.
        """
        if text:
            data = dict(date_from=self.start,
                        date_to=self.stop,
                        content=text,
                        is_sent=False)
            self.message.text = ""
            current_day = self.start.rsplit(" ", 1)[0]
            try:
                existing_data = DB.store_get(current_day)
            except KeyError:
                existing_data = []
            existing_data.append(data)
            DB.store_put(current_day, existing_data)
            DB.store_sync()
            if ACTIVE_STYLE == "style1":
                self.switch_screen('action')

    def on_mouse_pos(self, *args):
        """
        hover action handling, for capable buttons.
        """
        mouse_position = args[1]
        buttons = filter(lambda x: x.pos[0] <= mouse_position[0] <= x.ranged[0] and
                         x.pos[1] <= mouse_position[1] <= x.ranged[1],
                         self.buttons)
        button = None
        if buttons and 149 > mouse_position[1] > 1 and 299 > mouse_position[0] > 1 :
            button = buttons[0]
        for but in self.buttons:
            if but != button:
                but.inactive = True
            else:
                but.inactive = False

class PomodoroApp(App):

    def __init__(self, *args, **kwargs):
        super(PomodoroApp, self).__init__(*args, **kwargs)
        styles = {"style1": STYLE1, "style2": STYLE2}
        Builder.load_file(styles[ACTIVE_STYLE])
        self.icon = ICON_PATH
        self.title = "Pomodoro"

    def build(self):
        layout = Pomodoro()
        if ACTIVE_STYLE == "style2":
            Window.bind(mouse_pos=layout.on_mouse_pos)
        return layout

if __name__ == "__main__":
    """
    Window sizes and wanted skills are set, then app calls
    """
    styles = {"style1": WINDOW_SIZE_1, "style2": WINDOW_SIZE_2}
    Window.size = styles[ACTIVE_STYLE]
    Window.clearcolor = (.98, .98, .98, 1)
    Window.borderless = False
    Config.set('kivy', 'desktop', 1)
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'resizable', 0)

    PomodoroApp().run()
