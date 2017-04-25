from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
import time

id_1 = bytes(b'7F001AFC68')  ## salmon
id_2 = bytes(b'7F001B20C4')  ## whale
id_3 = bytes(b'7F001B3B09')  ## penguin

kv = '''
<CameraScreen>:
    orientation: 'vertical'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        size_hint_x: .5
        height: '32dp'
        Label:
            text: 'Name: '
        TextInput:
            id: name_input

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        size_hint_x: .5
        height: '32dp'
        Label:
            text: 'Email: '
        TextInput:
            id: email_input

    Camera:
        id: camera
        resolution: 800, 600

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '48dp'
        Button:
            text: 'Capture'
            on_press: self.parent.parent.capture()
'''
Builder.load_string(kv)

class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

class CameraScreen(BoxLayout):
    # def __init__(self, animal, **kwargs):
    #     self.animal = animal

    def capture(self):
        print("Captured")
        camera = self.ids['camera']
        name = self.ids['name_input']
        email = self.ids['email_input']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_me.png")

    # def send_email(self):


class ExitApp(App):
    def build(self):
        self.root = root = RootWidget()
        self.camera_screen = CameraScreen()

        self.root.add_widget(self.camera_screen)
        self.allow_scan = True

    # def get_rfid(self, dt):
    #     if self.allow_scan:  ## only read input if allowing scan
    #         rfid = read_rfid()
    #         if rfid:
    #             if rfid == id_1:
    #                 self.show_salmon()
    #             elif rfid == id_2:
    #                 self.show_whale()
    #             elif rfid == id_3:
    #                 self.show_penguin()



if __name__ == '__main__':
    ExitApp().run()
