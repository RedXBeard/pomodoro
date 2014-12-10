import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from time import strftime, gmtime
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.config import Config
from config import *

Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'resizable', 0)

class Pomodoro(BoxLayout):
    time_period = NumericProperty(TIME_PERIOD)
    time_display = StringProperty()
    rotation = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Pomodoro, self).__init__(*args, **kwargs)
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.animation = None
        self.clock = SoundLoader.load('assets/clock.wav')
        self.alarm = SoundLoader.load('assets/alarm.wav')
        self.perrotation = Vector(1, 1).angle(
            Vector(1, 1).rotate(360 / float(self.time_period)))

        # Default displayed numbers as minutes added within rule.
        for i in range(1, 5):
            pos = Vector(0, 70).rotate(self.perrotation * (self.time_period / 5) * i)
            display_time = int(strftime('%M:%S', gmtime((self.time_period / 5) * i)).split(":")[0])
            label = Label(text="[color=000000]%s min.[/color]"%display_time,
                          markup=True, pos=pos, size=(10,10),
                          font_name=KIVY_DEFAULT_FONT)
            self.floatlayout.add_widget(label)

    def start_animation(self):
        Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)
        self.start_button.disabled = True

    def decrease_minutes(self):
        if self.time_period == 0:
            self.reset_time()
        else:
            self.clock.stop()
            self.clock.play()
            self.rotation += self.perrotation
            self.time_period -= 1
            self.time_display = strftime('%M:%S', gmtime(self.time_period))
            if self.animation:
                self.animation.stop(self)
            self.animation = Animation(
                rotation=self.rotation, d=1500, t='out_quad', s=1)
            self.animation.start(self)
            Clock.schedule_once(lambda dt: self.decrease_minutes(), 1)

    def reset_time(self):
        self.clock.stop()
        self.alarm.play()
        self.time_period = TIME_PERIOD
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.start_button.disabled = False
        self.rotation = 0


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
