from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.uix.screenmanager import SlideTransition
from time import strftime, gmtime
from config import *
from datetime import datetime

Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'resizable', 0)


class Pomodoro(BoxLayout):
    time_period = NumericProperty()
    time_display = StringProperty()
    rotation = NumericProperty(0)
    start_time = NumericProperty()
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

        # Default displayed numbers as minutes added within rule.
#        for i in range(0, 5):
#            pos = Vector(0, 80).rotate(self.perrotation * (self.time_period / 5) * i)
#            display_time = int(strftime('%M:%S', gmtime((self.time_period / 5) * i)).split(":")[0])
#            label = Label(text="[color=000000]%s[/color]"%display_time,
#                          markup=True, pos=pos, size=(10,10),
#                          font_name=KIVY_DEFAULT_FONT)
#            self.floatlayout.add_widget(label)

    def start_animation(self):
        if self.state == "work":
            self.start = str(datetime.now()).rsplit('.', 1)[0]
        Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)
        self.start_button.disabled = True

    def decrease_minutes(self):
        if self.time_period < 1:
            self.rotation = 0
            self.reset_time()
        else:
            self.clock.stop()
            self.clock.play()

            self.rotation += self.perrotation
            self.time_period -= 1
            self.time_display = strftime('%M:%S', gmtime(self.time_period))

            if self.animation:
                self.animation.stop(self)
            self.animation = Animation(rotation=self.rotation, d=1)
            self.animation.start(self)

            if self.state == "work" and self.time_period < 1:
                self.stop = str(datetime.now()).rsplit('.', 1)[0]

            Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)

    def switch_screen(self, screen):
        self.sm.transition = SlideTransition(direction='up')
        self.sm.current = screen

    def set_clock(self):
        self.start_time = int(
            strftime('%M:%S', gmtime(self.time_period)).split(":")[0])
        self.perrotation = Vector(1, 1).angle(
            Vector(1, 1).rotate(360 / float(self.time_period)))

    def set_to_workstate(self):
        self.state = "work"
        self.time_period = WORK_TIME_PERIOD
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.sprint_count += 1
        self.set_clock()
        self.switch_screen('start')

    def set_to_breakstate(self):
        self.state = "break"
        self.time_period = BREAK_TIME_PERIOD * self.sprint_count
        self.sprint_count = 0
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.set_clock()
        self.switch_screen('start')

    def reset_time(self):
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
        on_off = 0 if state == "down" else 1
        if self.clock:
            self.clock.volume = on_off
        if self.alarm:
            self.alarm.volume = on_off

    def keep_info(self, text):
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

    def build(self):
        Window.size = (200, 240)
        Window.fullscreen = 0
        Window.resizable = 0
        return Pomodoro()

if __name__ == "__main__":
    PomodoroApp().run()
