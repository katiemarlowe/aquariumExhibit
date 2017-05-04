from rfid_reader import *
from send_email import *
from send_sms import *
import re
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# id_1 = bytes(b'7F001AFC68')  ## salmon
id_2 = bytes(b'7F001B20C4')  ## whale
id_3 = bytes(b'7F001B3B09')  ## penguin
id_1 = bytes(b'82003BADA1')

kv = '''
<CameraScreen>:
    orientation: 'vertical'

    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Enter your name and email to have your snapshot and\\neverything you have learned about your animal sent to you'
            font_size: '40pt'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '32dp'
        Label:
            text: 'Name: '
            size_hint_x: None
            width: '100dp'
        TextInput:
            id: name_input
            size_hint_x: None
            width: '150dp'
            focus: True
            write_tab: False

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '32dp'
        Label:
            text: 'Email: '
            size_hint_x: None
            width: '100dp'
        TextInput:
            id: email_input
            size_hint_x: None
            width: '150dp'
            write_tab: False

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '32dp'
        Label:
            text: 'Mobile Number: '
            size_hint_x: None
            width: '100dp'
        TextInput:
            id: phone_input
            size_hint_x: None
            width: '150dp'

    BoxLayout:
        orientation: 'horizontal'
        Camera:
            id: camera
            resolution: 800, 600

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '100dp'
        Button:
            background_normal: 'img/exit-screen/capture.png'
            on_press: self.parent.parent.capture()
            size_hint_x: None
            size_hint_y: None
            height: '76.5dp'
            width: '347.5dp'
            pos_hint: {'center_x': .5}
'''
Builder.load_string(kv)

class RootWidget(FloatLayout):
    def __init__(self, app, **kwargs):
        self.app = app
        super(RootWidget, self).__init__(**kwargs)


class CameraScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)

    def capture(self):
        print("Captured")
        camera = self.ids['camera']
        name = self.ids['name_input'].text
        email = self.ids['email_input'].text
        phone_number = self.ids['phone_input'].text
        self.ids['name_input'].focus = True
        camera.export_to_png('snapshots/IMG'+name+'.png')
        self.ids['name_input'].text = ''
        self.ids['email_input'].text = ''
        self.parent.app.pic_captured(name, email, phone_number)

class ExitApp(App):
    def build(self):
        self.root = root = RootWidget(app=self)
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 1, .5)  # torquise
            self.rect = Rectangle(size=root.size, pos=root.pos)

        self.camera_screen = CameraScreen()
        self.exit_screen1 = self.ExitScreen1()
        self.exit_screen2 = self.ExitScreen2()
        
        self.root.add_widget(self.exit_screen1)
        self.allow_scan = True
        self.animal = None

        Clock.schedule_interval(self.get_rfid, 1.0)

    def get_rfid(self, dt):
        if self.allow_scan:  ## only read input if allowing scan
            rfid = read_rfid()
            if rfid:
                self.allow_scan = False
                if rfid == id_1:
                    self.animal = "Salmon"
                elif rfid == id_2:
                    self.animal = "Right Whale"
                elif rfid == id_3:
                    self.animal = "Rockhopper Penguin"
                self.root.remove_widget(self.exit_screen1)
                self.root.add_widget(self.camera_screen)

    def pic_captured(self, name, email, phone_number):
        self.root.remove_widget(self.camera_screen)
        self.root.add_widget(self.exit_screen2)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            send_email(self.animal, name, email)
        else:
            print('Email address not valid')
        if len(phone_number) == 10:
            send_sms(phone_number, self.animal)
        else:
            print('Phone number not valid')

    def restart(self, arg):
        self.root.remove_widget(self.exit_screen2)
        self.root.add_widget(self.exit_screen1)
        self.allow_scan = True

    def ExitScreen1(self):
        exit_screen = FloatLayout()
        exit_screen.add_widget(Image(source='img/exit-screen/exit-screens.png', pos_hint={'x':0, 'y':0}))
        return exit_screen

    def ExitScreen2(self):
        exit_screen = FloatLayout()
        exit_screen.add_widget(Image(source='img/exit-screen/exit-screens2.png', pos_hint={'x':0, 'y':0}))
        restart_button = Button(background_normal='img/exit-screen/restart-button.png', size_hint=(None, None), size=(695,153), pos_hint={'center_x': .5, 'y': .2})
        restart_button.bind(on_press=self.restart)
        exit_screen.add_widget(restart_button)
        return exit_screen

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    ExitApp().run()
