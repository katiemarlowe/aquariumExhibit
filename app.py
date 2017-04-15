import time
from rfid_reader import *
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

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


class AquariumApp(App):

    def build(self):
    	self.root = root = RootWidget()
    	self.rfid = None
    	root.bind(size=self._update_rect, pos=self._update_rect)

    	with root.canvas.before:
    		Color(0, 1, 1, .5)  # torquise
    		self.rect = Rectangle(size=root.size, pos=root.pos)

    	self.welcome_screen = self.WelcomeScreen()
    	root.add_widget(self.welcome_screen)

    	Clock.schedule_interval(self.get_rfid, 1.0)
    	print("RFID is: ", self.rfid)

    	# button = Button(text='Next', font_size=14, size_hint=(.1, .1))
    	self.salmon_threats_screen = self.SalmonThreatsScreen()
    	# root.add_widget(button)

    	# button.bind(on_press=lambda x: self.show_content(welcome_screen, salmon_threats_screen))



    	return root

    def get_rfid(self, dt):
    	rfid = read_rfid()
    	if rfid:
    		self.rfid = rfid
    		self.show_content(self.welcome_screen, self.salmon_threats_screen)

    def show_content(self, old_screen, new_screen):
    	self.root.remove_widget(old_screen)
    	self.root.add_widget(new_screen)

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

    def _update_rect(self, instance, value):
    	self.rect.pos = instance.pos
    	self.rect.size = instance.size

if __name__ == '__main__':
    AquariumApp().run()