from rfid_reader import *
from exit_utils import *
import re
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

id_3 = bytes(b'7F001AFC68')  ## penguin
id_2 = bytes(b'7F001B20C4')  ## whale
id_1 = bytes(b'7F001B3B09')  ## salmon
# id_1 = bytes(b'82003BADA1')

kv = '''
<CameraScreen>:
    orientation: 'vertical'

    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Take a photo with your animal!'
            font_size: '40pt'
            color: .15, .17, .47, 1
            bold: True

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

<EmailScreen>
    orientation: 'vertical'

    Label:
        text: 'You guys look great!'
        font_size: '30pt'
        pos_hint: {'center_x': .5, 'center_y': .9}
        color: .15, .17, .47, 1
        bold: True

    Label:
        text: 'Enter your email to get the photo and\\n more information about your animal'
        font_size: '30pt'
        pos_hint: {'center_x': .5, 'center_y': .5}
        color: .15, .17, .47, 1
        bold: True

    TextInput:
        id: email_input
        focus: True
        size_hint_x: None
        size_hint_y: None
        width: '500dp'
        height: '60dp'
        font_size: '30pt'
        pos_hint: {'center_x': .5, 'center_y': .4}
        write_tab: False

    Label:
        text: 'If you would like your photo texted to you\\n enter your mobile number below'
        font_size: '20pt'
        pos_hint: {'center_x': .5, 'center_y': .3}
        color: .15, .17, .47, 1
        bold: True

    TextInput:
        id: phone_input
        size_hint_x: None
        size_hint_y: None
        width: '500dp'
        height: '60dp'
        font_size: '30pt'
        pos_hint: {'center_x': .5, 'center_y': .2}
        write_tab: False

    Button:
        background_normal: 'img/exit-screen/next.png'
        on_press: self.parent.info()
        size_hint_x: None
        size_hint_y: None
        height: '90dp'
        width: '209.5dp'
        pos_hint: {'center_x': .5, 'center_y': .1}

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
        img_num = random.randint(10, 99)
        camera.export_to_png('snapshots/IMG'+str(img_num)+'.png')
        self.parent.app.pic_captured(img_num)

class EmailScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(EmailScreen, self).__init__(**kwargs)

    def info(self):
        email_addr = self.ids['email_input'].text
        phone_number = self.ids['phone_input'].text
        self.ids['email_input'].focus = True
        self.ids['email_input'].text = ''
        self.ids['phone_input'].text = ''
        self.parent.app.collect_info(email_addr, phone_number)
        

class ExitApp(App):
    def build(self):
        self.root = root = RootWidget(app=self)
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(1, 1, 1, 1)  # white
            self.rect = Rectangle(size=root.size, pos=root.pos)

        self.camera_screen = CameraScreen()
        self.email_screen = EmailScreen()
        self.exit_screen1 = self.ExitScreen1()
        self.exit_screen2 = self.ExitScreen2()
        
        self.root.add_widget(self.exit_screen1)
        self.allow_scan = True
        self.animal = None
        self.current_img_num = None
        self.current_image = None

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

    def pic_captured(self, img_num):
        self.root.remove_widget(self.camera_screen)
        self.root.add_widget(self.email_screen)
        save_photo(img_num)
        self.current_img_num = img_num
        self.current_image = Image(source='snapshots/IMG'+str(img_num)+'LOGO.png', pos_hint={'center_x': .5, 'center_y': .7}, size_hint=(None, None), size=(438.2, 246.4))
        self.email_screen.add_widget(self.current_image)

    def collect_info(self, email_addr, phone_number):
        self.root.remove_widget(self.email_screen)
        self.email_screen.remove_widget(self.current_image)
        self.root.add_widget(self.exit_screen2)
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_addr):
            send_email(self.animal, email_addr, self.current_img_num)
        else:
            print('Email address not valid')
        # if len(phone_number) == 10:
        if phone_number == '9174030096':
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
