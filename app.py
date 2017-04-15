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

# class WelcomeScreen(RelativeLayout):
# 	def __init__(self, **kwargs):
# 		super(WelcomeScreen, self).__init__(**kwargs)
# 		self.add_widget(Label(text='Welcome!'))

# class SalmonThreatsScreen(RelativeLayout):
# 	def __init__(self, **kwargs):
# 		super(SalmonThreatsScreen, self).__init__(**kwargs)
# 		self.add_widget(Label(text='Salmon Threats'))

class RootWidget(FloatLayout):
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)

# 	def update(self, dt):
# 		rfid = read_rfid()
# 		if rfid:
# 			print("Found RFID")
# 			self.rfid = rfid
# 			AquariumApp.show_content()
# 			print("Showing screen")
# 			time.sleep(5)
# 			print("Done showing")


class AquariumApp(App):

    def build(self):
        self.root = root = RootWidget()
        # self.rfid = None
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 1, .5)  # torquise
            self.rect = Rectangle(size=root.size, pos=root.pos)

        self.welcome_screen = self.WelcomeScreen()
        root.add_widget(self.welcome_screen)
        self.salmon_threats_screen = self.SalmonThreatsScreen()
        self.whale_threats_screen = self.WhaleThreatsScreen()
        self.penguin_threats_screen = self.PenguinThreatsScreen()

        self.show_salmon = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.salmon_threats_screen))
        self.show_whale = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.whale_threats_screen))
        self.show_penguin = Clock.create_trigger(partial(self.show_content, self.welcome_screen, self.penguin_threats_screen))
        # self.remove_salmon = Clock.create_trigger(partial(self.show_content, self.salmon_threats_screen, self.welcome_screen))

        Clock.schedule_interval(self.get_rfid, 1.0)
        return root

    def get_rfid(self, dt):
        rfid = read_rfid()
        if rfid:
            if rfid == id_1:
                self.show_salmon()
                # Clock.schedule_once(partial(self.show_content, self.salmon_threats_screen, self.welcome_screen), 5)
            elif rfid == id_2:
                self.show_whale()
                # Clock.schedule_once(partial(self.show_content, self.whale_threats_screen, self.welcome_screen), 5)
            elif rfid == id_3:
                self.show_penguin()
                # Clock.schedule_once(partial(self.show_content, self.penguin_threats_screen, self.welcome_screen), 5)


    def show_content(self, old_screen, new_screen, dt):
        self.root.remove_widget(old_screen)
        self.root.add_widget(new_screen)
        Clock.schedule_once(partial(self.show_content, new_screen, old_screen), 5)

    def wait_to_remove(self, trigger_event):
        Clock.schedule_once()

    def WelcomeScreen(self):
    	welcome_screen = FloatLayout()
    	welcome_screen.add_widget(Label(text='Welcome!'))
    	return welcome_screen

    def SalmonThreatsScreen(self):
    	salmon_threats_screen = FloatLayout()
    	salmon_threats_screen.add_widget(Label(text="Salmon Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
    	salmon_threats_screen.add_widget(Image(source='img/salmon.png', pos_hint={'x':0, 'y':0}))
    	salmon_threats_screen.add_widget(Label(text="Rising river temperatures", font_size=14, pos_hint={'x':0, 'y':-.2}))
    	salmon_threats_screen.add_widget(Label(text="Climate change", font_size=14, pos_hint={'x':0, 'y':-.25}))
    	salmon_threats_screen.add_widget(Label(text="Dams", font_size=14, pos_hint={'x':0, 'y':-.3}))
    	salmon_threats_screen.add_widget(Label(text="Fishing", font_size=14, pos_hint={'x':0, 'y':-.35}))
    	return salmon_threats_screen

    def WhaleThreatsScreen(self):
        whale_threats_screen = FloatLayout()
        whale_threats_screen.add_widget(Label(text="Whale Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
        return whale_threats_screen

    def PenguinThreatsScreen(self):
        penguin_threats_screen = FloatLayout()
        penguin_threats_screen.add_widget(Label(text="Penguin Threats", font_size=20, pos_hint={'x':0, 'y':.3}))
        return penguin_threats_screen

    def _update_rect(self, instance, value):
    	self.rect.pos = instance.pos
    	self.rect.size = instance.size

if __name__ == '__main__':
    AquariumApp().run()