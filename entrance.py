from rfid_reader import *
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from functools import partial
from kivy.uix.button import Button

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

        self.whale_screen = self.WhaleScreen()
        self.salmon_screen = self.SalmonScreen()

        self.keep_salmon_screen = self.KeepSalmonScreen()

        self.show_salmon = Clock.create_trigger(partial(self.show_animal, self.salmon_screen))

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
                    self.show_salmon()
                elif rfid == id_2:
                    self.show_whale()
                elif rfid == id_3:
                    self.show_penguin()

    def show_animal(self, new_screen, dt):
        self.allow_scan = False
        self.root.remove_widget(self.select_animal_screen)
        self.root.add_widget(new_screen)

    def keep_animal(self, instance, animal):
        if animal == 'salmon':
            self.root.remove_widget(self.salmon_screen)
            self.root.add_widget(self.keep_salmon_screen)

    def dont_keep_animal(self, instance, animal):
        if animal == 'salmon':
            self.root.remove_widget(self.salmon_screen)
        self.root.add_widget(self.select_animal_screen)
        self.allow_scan = True

    def done_animal(self, instance, animal):
        if animal == 'salmon':
            self.root.remove_widget(self.keep_salmon_screen)
        self.root.add_widget(self.select_animal_screen)
        self.allow_scan = True

    def SelectAnimalScreen(self):
        select_animal_screen = FloatLayout()
        select_animal_screen.add_widget(Label(text='select an animal from the wall', font_size='40pt'))
        return select_animal_scree

    def SalmonScreen(self):
        salmon_screen = FloatLayout()
        salmon_screen.add_widget(Label(text="that's a salmon!", font_size='40pt'))
        salmon_screen.add_widget(Label(text="keep?", font_size='20pt', pos_hint={'y':-.1}))
        yes_button = Button(text='Yes', font_size='32pt', pos_hint={'center_x':.3, 'y':.2}, size_hint=(.2, .1))
        no_button = Button(text='No', font_size='32pt', pos_hint={'center_x':.7, 'y':.2}, size_hint=(.2, .1))
        yes_button.bind(on_press=partial(self.keep_animal, animal='salmon'))
        no_button.bind(on_press=partial(self.dont_keep_animal, animal='salmon'))
        salmon_screen.add_widget(yes_button)
        salmon_screen.add_widget(no_button)
        return salmon_screen

    def KeepSalmonScreen(self):
        keep_salmon_screen = FloatLayout()
        keep_salmon_screen.add_widget(Label(text='Great Choice!'))
        done_button = Button(text='Thanks', font_size='32pt', pos_hint={'center_x':.5, 'y':.2}, size_hint=(.2, .1))
        done_button.bind(on_press=partial(self.done_animal, animal='salmon'))
        keep_salmon_screen.add_widget(done_button)
        return keep_salmon_screen

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    EntranceApp().run()