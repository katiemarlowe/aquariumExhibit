from rfid_reader import *
from send_email import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

id_1 = bytes(b'7F001AFC68')  ## salmon
id_2 = bytes(b'7F001B20C4')  ## whale
id_3 = bytes(b'7F001B3B09')  ## penguin

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
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

class CameraScreen(BoxLayout):
    def __init__(self, animal, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        self.animal = animal

    def capture(self):
        print("Captured")
        camera = self.ids['camera']
        name = self.ids['name_input'].text
        email = self.ids['email_input'].text
        camera.export_to_png('snapshots/'+name+'.png')
        send_email(self.animal, name, email)

class ExitApp(App):
    def build(self):
        self.root = root = RootWidget()
        self.exit_screen = self.ExitScreen()
        
        self.root.add_widget(self.exit_screen)
        self.allow_scan = True

        Clock.schedule_interval(self.get_rfid, 1.0)

    def get_rfid(self, dt):
        if self.allow_scan:  ## only read input if allowing scan
            rfid = read_rfid()
            if rfid:
                self.allow_scan = False
                if rfid == id_1:
                    animal = "Salmon"
                elif rfid == id_2:
                    animal = "Right Whale"
                elif rfid == id_3:
                    animal = "Rockhopper Penguin"
                self.root.remove_widget(self.exit_screen)
                self.root.add_widget(CameraScreen(animal))

    def ExitScreen(self):
        exit_screen = FloatLayout()
        exit_screen.add_widget(Label(text='Aquarium Exit - Scan Your Animal', font_size='24pt'))
        return exit_screen

if __name__ == '__main__':
    ExitApp().run()
