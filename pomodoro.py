import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from time import strftime, gmtime
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

KIVY_VERSION = kivy.__version__
TIME_PERIOD = 30

class Pomodoro(BoxLayout):
    time_period = NumericProperty(TIME_PERIOD)
    time_display = StringProperty()
    rotation = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Pomodoro, self).__init__(*args, **kwargs)
        self.time_display = strftime('%M:%S', gmtime(self.time_period))
        self.animation = None
        self.clock = SoundLoader.load('clock.wav')
        self.alarm = SoundLoader.load('alarm.wav')
        self.perrotation = Vector(1, 1).angle(
            Vector(1, 1).rotate(360 / float(self.time_period)))

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
