from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout

class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

class EntranceApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 1, .5)  # torquise
            self.rect = Rectangle(size=root.size, pos=root.pos)

        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    EntranceApp().run()