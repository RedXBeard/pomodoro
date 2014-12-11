from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.uix.screenmanager import SlideTransition
from time import strftime, gmtime
from datetime import datetime
from config import *


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

    def __init__(self, *args, **kwargs):
        super(Pomodoro, self).__init__(*args, **kwargs)
        self.set_to_workstate()
        self.animation = None
        self.clock = SoundLoader.load('assets/clock.wav')
        self.alarm = SoundLoader.load('assets/alarm.wav')
        self.sm.current = 'start'

    def start_animation(self):
        """
        starts animation for rotation, if state is on 'work'
        then start date should be taken to log pomodoro.
        other then stop date must be reset in each starting animation action.
        """
        if self.state == "work":
            self.start = str(datetime.now()).rsplit('.', 1)[0]
        self.stop = ""
        Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)
        self.start_button.disabled = True

    def decrease_minutes(self):
        """
        until the rotation count reaches the end
        minutes and rotation should be continue.
        At the end pomodoro stop date must be taken too
        sounds should also be handled.
        """
        if self.time_period < 1:
            self.rotation = 0
            self.reset_time()
        else:
            self.clock.stop()
            self.clock.play()

            self.rotation += self.perrotation
            self.time_period -= 1
            self.time_display = strftime('%M:%S', gmtime(self.time_period))
            self.time_minute, self.time_second = self.time_display.split(':')

            if self.animation:
                self.animation.stop(self)
            self.animation = Animation(rotation=self.rotation, d=1)
            self.animation.start(self)

            if self.state == "work" and self.time_period < 1:
                self.stop = str(datetime.now()).rsplit('.', 1)[0]

            Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)

    def switch_screen(self, screen):
        """
        action screens rotation handling
        """
        self.sm.transition = SlideTransition(direction='up')
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
        self.start_button.disabled = False
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
            self.switch_screen('action')

class PomodoroApp(App):

    def __init__(self, *args, **kwargs):
        super(PomodoroApp, self).__init__(*args, **kwargs)
        Builder.load_file('pomodoro_main.kv')
        self.icon = ICON_PATH
        self.title = "Pomodoro"

    def build(self):
        return Pomodoro()

if __name__ == "__main__":
    """
    Window sizes and wanted skills are set, then app calls
    """
    Window.size = (200, 240)
    Window.borderless = False
    Window.clearcolor = (1,1,1,1)
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'resizable', 0)
    PomodoroApp().run()
