import time
from rfid_reader import *
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

id_1 = bytes(b'7F001AFC68')
id_2 = bytes(b'7F001B20C4')
id_3 = bytes(b'7F001B3B09')

KIOSK_MODE = "THREATS"  ## "FOOD", "FAMILY", or "THREATS"


class RootWidget(FloatLayout):
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)


class AquariumApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 1, .5)  # torquise
            self.rect = Rectangle(size=root.size, pos=root.pos)

        self.welcome_screen = self.WelcomeScreen()
        root.add_widget(self.welcome_screen)
        self.showing_content = False  ## whether the app is currently showing content

        self.salmon_screen = self.SalmonScreen()
        self.whale_screen = self.WhaleScreen()
        self.penguin_screen = self.PenguinScreen()

        self.show_salmon = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.salmon_screen))
        self.show_whale = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.whale_screen))
        self.show_penguin = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.penguin_screen))

        Clock.schedule_interval(self.get_rfid, 1.0)
        return root

    def get_rfid(self, dt):
        if not self.showing_content:  ## don't read input if currently showing content
            rfid = read_rfid()
            if rfid:
                if rfid == id_1:
                    self.show_salmon()
                elif rfid == id_2:
                    self.show_whale()
                elif rfid == id_3:
                    self.show_penguin()

    def show_content(self, old_screen, new_screen, dt, remove=False):
        self.showing_content = False
        self.root.remove_widget(old_screen)
        self.root.add_widget(new_screen)
        if not remove:
            self.showing_content = True
            Clock.schedule_once(partial(self.show_content, new_screen, old_screen, remove=True), 5)

    def WelcomeScreen(self):
    	welcome_screen = FloatLayout()
    	welcome_screen.add_widget(Label(text='Welcome!'))
    	return welcome_screen

    def SalmonScreen(self):
        salmon_screen = FloatLayout()
        if KIOSK_MODE == "THREATS":
            salmon_screen.add_widget(Label(text="Salmon Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
            salmon_screen.add_widget(Image(source='img/salmon.png', pos_hint={'x':0, 'y':0}))
            salmon_screen.add_widget(Label(text="Rising river temperatures", font_size=14, pos_hint={'x':0, 'y':-.2}))
            salmon_screen.add_widget(Label(text="Climate change", font_size=14, pos_hint={'x':0, 'y':-.25}))
            salmon_screen.add_widget(Label(text="Dams", font_size=14, pos_hint={'x':0, 'y':-.3}))
            salmon_screen.add_widget(Label(text="Fishing", font_size=14, pos_hint={'x':0, 'y':-.35}))
        elif KIOSK_MODE == "FOOD":
            salmon_screen.add_widget(Label(text="Salmon Food", font_size=20, pos_hint={'x':0, 'y':.3}))
        elif KIOSK_MODE == "FAMILY":
            salmon_screen.add_widget(Label(text="Salmon Family", font_size=20, pos_hint={'x':0, 'y':.3}))
        return salmon_screen

    def WhaleScreen(self):
        whale_screen = FloatLayout()
        if KIOSK_MODE == "THREATS":
            whale_screen.add_widget(Label(text="Whale Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
        elif KIOSK_MODE == "FOOD":
            whale_screen.add_widget(Label(text="Whale Food", font_size=20, pos_hint={'x':0, 'y':.3}))
        elif KIOSK_MODE == "FAMILY":
            whale_screen.add_widget(Label(text="Whale Family", font_size=20, pos_hint={'x':0, 'y':.3}))
        return whale_screen

    def PenguinScreen(self):
        penguin_screen = FloatLayout()
        if KIOSK_MODE == "THREATS":
            penguin_screen.add_widget(Label(text="Penguin Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
        elif KIOSK_MODE == "FOOD":
            penguin_screen.add_widget(Label(text="Penguin Food", font_size=20, pos_hint={'x':0, 'y':.3}))
        elif KIOSK_MODE == "FAMILY":
            penguin_screen.add_widget(Label(text="Penguin Family", font_size=20, pos_hint={'x':0, 'y':.3}))
        return penguin_screen

    def _update_rect(self, instance, value):
    	self.rect.pos = instance.pos
    	self.rect.size = instance.size

if __name__ == '__main__':
    AquariumApp().run()