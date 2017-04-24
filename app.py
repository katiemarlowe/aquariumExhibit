import time
import argparse
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
from kivy.uix.video import Video
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup

id_1 = bytes(b'7F001AFC68')  ## salmon
# id_2 = bytes(b'82003BADA1')  
id_2 = bytes(b'7F001B20C4')  ## whale
id_3 = bytes(b'7F001B3B09')  ## penguin

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="", type=str)
KIOSK_MODE = parser.parse_args().mode  ## "FOOD", "FAMILY", or "THREATS"
print('KIOSK MODE: ', KIOSK_MODE)

HAS_VIDEO = {'FOOD': {'salmon': None, 'whale': None, 'penguin': None}, 
            'FAMILY': {
                'salmon': Video(source="img/salmon-family.mov", pos_hint={'x':0, 'y':0}, options={'eos': 'loop'}),
                'whale': None, 
                'penguin': Video(source="img/penguin-family.mov", pos_hint={'x':0, 'y':0}, options={'eos': 'loop'})},
            'THREATS': {
                'salmon': None, 
                'whale': Video(source="img/whale-threats.mov", pos_hint={'x':0, 'y':0}, options={'eos': 'loop'}), 
                'penguin': None}}

icon_noscan = Image(source='img/icon-noscan.png', pos_hint={'x':.42, 'y':-.36})
icon_scan = Image(source='img/icon-scan.png', pos_hint={'x':.42, 'y':-.36})
icon_welcome_scan = Image(source='img/icon-welcome-scan.png', pos_hint={'x':.42, 'y':-.36})
# if KIOSK_MODE == "FAMILY":
    # whale_noscan = Image(source='img/whale-family-noscan.png', pos_hint={'x':0, 'y':0})
    # whale_scan = Image(source='img/whale-family-scan.png', pos_hint={'x':0, 'y':0})
# if KIOSK_MODE == "FOOD":
    # whale_noscan = Image(source='img/whale-food-noscan.png', pos_hint={'x':0, 'y':0})
    # whale_scan = Image(source='img/whale-food-scan.png', pos_hint={'x':0, 'y':0})
    # salmon_noscan = Image(source='img/salmon-food-noscan.png', pos_hint={'x':0, 'y':0})
    # salmon_scan = Image(source='img/salmon-food-scan.png', pos_hint={'x':0, 'y':0})
    
    # penguin_noscan = Image(source='img/penguin-food-noscan.png', pos_hint={'x':0, 'y':0})
    # penguin_scan = Image(source='img/penguin-food-scan.png', pos_hint={'x':0, 'y':0})
# if KIOSK_MODE == "THREATS":
    # penguin_noscan = Image(source='img/penguin-threats-noscan.png', pos_hint={'x':0, 'y':0})
    # penguin_scan = Image(source='img/penguin-threats-scan.png', pos_hint={'x':0, 'y':0})
    # salmon_noscan = Image(source='img/salmon-threats-noscan.png', pos_hint={'x':0, 'y':0})
    # salmon_scan = Image(source='img/salmon-threats-scan.png', pos_hint={'x':0, 'y':0})

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
        self.allow_scan = True  ## whether the app currently allows new scan
        self.current_screen = self.welcome_screen
        self.current_vid_playing = None

        self.salmon_screen = self.SalmonScreen()
        self.whale_screen = self.WhaleScreen()
        self.penguin_screen = self.PenguinScreen()

        self.show_salmon = Clock.create_trigger(partial(self.show_content, self.salmon_screen))
        self.show_whale = Clock.create_trigger(partial(self.show_content, self.whale_screen))
        self.show_penguin = Clock.create_trigger(partial(self.show_content, self.penguin_screen))

        Clock.schedule_interval(self.get_rfid, 1.0)
        return root

    def get_rfid(self, dt):
        if self.allow_scan:  ## only read input if allowing scan
            rfid = read_rfid()
            if rfid:
                self.current_screen.remove_widget(icon_scan)
                if self.current_vid_playing:
                    self.current_vid_playing.state = 'stop'
                    self.current_vid_playing = None
                    # self.current_screen.remove_widget(icon_scan)
                if rfid == id_1:
                    self.show_salmon()
                elif rfid == id_2:
                    self.show_whale()
                elif rfid == id_3:
                    self.show_penguin()

    def show_content(self, new_screen, dt):
        if new_screen == self.whale_screen:
            animal = 'whale'
        if new_screen == self.salmon_screen:
            animal = 'salmon'
        if new_screen == self.penguin_screen:
            animal = 'penguin'
        
        if HAS_VIDEO[KIOSK_MODE][animal]:
            HAS_VIDEO[KIOSK_MODE][animal].state = 'play'
            self.current_vid_playing = HAS_VIDEO[KIOSK_MODE][animal]

        self.allow_scan = False
        self.root.remove_widget(self.current_screen)
        self.root.add_widget(new_screen)
        self.current_screen = new_screen
        self.current_screen.add_widget(icon_noscan)
        Clock.schedule_once(self.change_allow_scan, 10)

        # if self.current_vid_playing:
        #     self.current_screen.add_widget(icon_noscan)

    def change_allow_scan(self, dt):
        self.allow_scan = not self.allow_scan
        # if self.current_vid_playing:
        self.current_screen.remove_widget(icon_noscan)
        self.current_screen.add_widget(icon_scan)
        # if self.current_screen == self.whale_screen and not self.current_vid_playing:
        #     self.whale_screen.remove_widget(whale_noscan)
        #     self.whale_screen.add_widget(whale_scan)
        # if self.current_screen == self.salmon_screen and not self.current_vid_playing:
        #     self.salmon_screen.remove_widget(salmon_noscan)
        #     self.salmon_screen.add_widget(salmon_scan)
        # if self.current_screen == self.penguin_screen and not self.current_vid_playing:
        #     self.penguin_screen.remove_widget(penguin_noscan)
        #     self.penguin_screen.add_widget(penguin_scan)

    def WelcomeScreen(self):
        welcome_screen = FloatLayout()
        welcome_screen.add_widget(Label(text='Welcome!', font_size='40pt'))
        welcome_screen.add_widget(icon_welcome_scan)
        return welcome_screen

    def SalmonScreen(self):
        salmon_screen = FloatLayout()
        if KIOSK_MODE == "FAMILY":
            salmon_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['salmon'])
        if KIOSK_MODE == "FOOD":
            salmon_screen.add_widget(Image(source='img/salmon-food-noscan.png', pos_hint={'x':0, 'y':0}))
            salmon_icon_1 = Button(background_normal='img/test-icon.png', pos_hint={'x':.8, 'y':.4}, size_hint=(.1, .1))
            salmon_text_1 = ModalView(background='img/test-text.png', pos_hint={'x':.1, 'y':.1}, size_hint=(None, None), size=(400, 400))
            salmon_icon_1.bind(on_press=salmon_text_1.open)
            salmon_screen.add_widget(salmon_icon_1)
        if KIOSK_MODE == "THREATS":
            salmon_screen.add_widget(Image(source='img/salmon-threats-noscan.png', pos_hint={'x':0, 'y':0}))
        return salmon_screen

    def WhaleScreen(self):
        whale_screen = FloatLayout()
        if KIOSK_MODE == "THREATS":
            whale_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['whale'])
        if KIOSK_MODE == "FAMILY":
            whale_screen.add_widget(Image(source='img/whale-family-noscan.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "FOOD":
            whale_screen.add_widget(Image(source='img/whale-food-noscan.png', pos_hint={'x':0, 'y':0}))
        return whale_screen

    def PenguinScreen(self):
        penguin_screen = FloatLayout()
        if KIOSK_MODE == "FAMILY":
            penguin_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['penguin'])
        if KIOSK_MODE == "FOOD":
            penguin_screen.add_widget(Image(source='img/penguin-food-noscan.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "THREATS":
            penguin_screen.add_widget(Image(source='img/penguin-threats-noscan.png', pos_hint={'x':0, 'y':0}))
        return penguin_screen

    def _update_rect(self, instance, value):
    	self.rect.pos = instance.pos
    	self.rect.size = instance.size

if __name__ == '__main__':
    AquariumApp().run()