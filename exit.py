from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
import time


kv = '''
<CameraScreen>:
    orientation: 'vertical'

    Camera:
        id: camera
        resolution: 399, 299

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
    def capture(self):
        print("Captured")
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))

class ExitApp(App):
    def build(self):
        self.root = root = RootWidget()
        self.camera_screen = CameraScreen()

        self.root.add_widget(self.camera_screen)



if __name__ == '__main__':
    ExitApp().run()
