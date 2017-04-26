from rfid_reader import *
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from functools import partial
from kivy.uix.button import Button
from kivy.uix.image import Image

id_1 = bytes(b'7F001AFC68')  ## salmon
id_2 = bytes(b'7F001B20C4')  ## whale
id_3 = bytes(b'7F001B3B09')  ## penguin

class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

class EntranceApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        self.select_animal_screen = self.SelectAnimalScreen()
        root.add_widget(self.select_animal_screen)
        self.allow_scan = True
        self.cur_animal_screen = None

        self.whale_screen = self.WhaleScreen()
        self.salmon_screen = self.SalmonScreen()
        self.penguin_screen = self.PenguinScreen()

        self.keep_screen = self.KeepScreen()

        with root.canvas.before:
            Color(0, 1, 1, .5)  # torquise
            self.rect = Rectangle(size=root.size, pos=root.pos)

        Clock.schedule_interval(self.get_rfid, 1.0)

        return root

    def get_rfid(self, dt):
        if self.allow_scan:  ## only read input if allowing scan
            rfid = read_rfid()
            if rfid:
                if rfid == id_1:
                    self.cur_animal_screen = self.salmon_screen
                elif rfid == id_2:
                    self.cur_animal_screen = self.whale_screen
                elif rfid == id_3:
                    self.cur_animal_screen = self.penguin_screen
                self.show_animal(self.cur_animal_screen)

    def show_animal(self, new_screen):
        self.allow_scan = False
        self.root.remove_widget(self.select_animal_screen)
        self.root.add_widget(new_screen)

    def keep_animal(self, instance, animal):
        self.root.remove_widget(self.cur_animal_screen)
        self.root.add_widget(self.keep_screen)

    def dont_keep_animal(self, instance):
        self.root.remove_widget(self.cur_animal_screen)
        self.root.add_widget(self.select_animal_screen)
        self.allow_scan = True

    def done_animal(self, instance):
        self.root.remove_widget(self.keep_screen)
        self.root.add_widget(self.select_animal_screen)
        self.allow_scan = True
        
    def SelectAnimalScreen(self):
        select_animal_screen = FloatLayout()
        select_animal_screen.add_widget(Image(source='img/entrance-screen/intro-kiosk.png'))
        return select_animal_screen

    def SalmonScreen(self):
        salmon_screen = FloatLayout()
        salmon_screen.add_widget(Image(source='img/entrance-screen/intro-kiosk5.png'))
        yes_button = Button(background_normal='img/entrance-screen/yes.png', pos_hint={'center_x':.3, 'y':.2}, size_hint=(.2, .1))
        no_button = Button(background_normal='img/entrance-screen/no.png', pos_hint={'center_x':.7, 'y':.2}, size_hint=(.2, .1))
        yes_button.bind(on_press=self.keep_animal)
        no_button.bind(on_press=self.dont_keep_animal)
        salmon_screen.add_widget(yes_button)
        salmon_screen.add_widget(no_button)
        return salmon_screen

    def WhaleScreen(self):
        whale_screen = FloatLayout()
        whale_screen.add_widget(Image(source='img/entrance-screen/intro-kiosk2.png'))
        yes_button = Button(background_normal='img/entrance-screen/yes.png', pos_hint={'center_x':.3, 'y':.2}, size_hint=(.2, .1))
        no_button = Button(background_normal='img/entrance-screen/no.png', pos_hint={'center_x':.7, 'y':.2}, size_hint=(.2, .1))
        yes_button.bind(on_press=partial(self.keep_animal, animal='whale'))
        no_button.bind(on_press=partial(self.dont_keep_animal, animal='whale'))
        whale_screen.add_widget(yes_button)
        whale_screen.add_widget(no_button)
        return whale_screen

    def PenguinScreen(self):
        penguin_screen = FloatLayout()
        penguin_screen.add_widget(Image(source='img/entrance-screen/intro-kiosk4.png'))
        yes_button = Button(background_normal='img/entrance-screen/yes.png', pos_hint={'center_x':.3, 'y':.2}, size_hint=(.2, .1))
        no_button = Button(background_normal='img/entrance-screen/no.png', pos_hint={'center_x':.7, 'y':.2}, size_hint=(.2, .1))
        yes_button.bind(on_press=self.keep_animal)
        no_button.bind(on_press=self.dont_keep_animal)
        penguin_screen.add_widget(yes_button)
        penguin_screen.add_widget(no_button)
        return penguin_screen

    def KeepScreen(self):
        keep_screen = FloatLayout()
        keep_screen.add_widget(Image(source='img/entrance-screen/intro-kiosk3.png'))
        done_button = Button(background_normal='img/entrance-screen/thanks.png', pos_hint={'center_x':.5, 'y':.2}, size_hint=(.2, .1))
        done_button.bind(on_press=self.done_animal)
        keep_screen.add_widget(done_button)
        return keep_screen

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    EntranceApp().run()