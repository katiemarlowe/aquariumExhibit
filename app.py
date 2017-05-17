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

# id_3 = bytes(b'7F001AFC68')  ## penguin
id_2 = bytes(b'7F001B20C4')  ## whale
id_1 = bytes(b'7F001B3B09')  
id_3 = bytes(b'82003BADA1')

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

# icon_noscan = Image(source='img/icon-noscan.png', pos_hint={'x':.42, 'y':-.36})
icon_scan = Image(source='img/icon-scan.png', pos_hint={'x':.42, 'y':-.36})
icon_welcome_scan = Image(source='img/icon-welcome-scan.png', pos_hint={'x':.42, 'y':-.36})
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
        self.salmon_quiz = self.SalmonQuiz()
        self.whale_screen = self.WhaleScreen()
        self.whale_quiz = self.WhaleQuiz()
        self.penguin_screen = self.PenguinScreen()
        self.penguin_quiz = self.PenguinQuiz()

        self.whale_right = self.WhaleRight()
        self.whale_wrong = self.WhaleWrong()
        self.salmon_right = self.SalmonRight()
        self.salmon_wrong = self.SalmonWrong()
        self.penguin_right = self.PenguinRight()
        self.penguin_wrong = self.PenguinWrong()

        self.show_salmon = Clock.create_trigger(partial(self.show_content, self.salmon_screen))
        self.show_whale = Clock.create_trigger(partial(self.show_content, self.whale_screen))
        self.show_penguin = Clock.create_trigger(partial(self.show_content, self.penguin_screen))

        Clock.schedule_interval(self.get_rfid, 1.0)
        return root

    def get_rfid(self, dt):
        if self.allow_scan:  ## only read input if allowing scan
            rfid = read_rfid()
            if rfid:
                # self.current_screen.remove_widget(icon_scan)
                if self.current_vid_playing:
                    self.current_vid_playing.state = 'stop'
                    self.current_vid_playing = None
                    self.current_screen.remove_widget(icon_scan)
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
            new_screen.add_widget(icon_scan)

        self.allow_scan = False
        self.root.remove_widget(self.current_screen)
        self.root.add_widget(new_screen)
        self.current_screen = new_screen

        if HAS_VIDEO[KIOSK_MODE][animal]:
            self.allow_scan = True
        # self.current_screen.add_widget(icon_noscan)
        # Clock.schedule_once(self.change_allow_scan, 10)

        # if self.current_vid_playing:
        #     self.current_screen.add_widget(icon_noscan)

    # def change_allow_scan(self, dt):
    #     self.allow_scan = not self.allow_scan
        # if self.current_vid_playing:
        # self.current_screen.remove_widget(icon_noscan)
        # self.current_screen.add_widget(icon_scan)
        # if self.current_screen == self.whale_screen and not self.current_vid_playing:
        #     self.whale_screen.remove_widget(whale_noscan)
        #     self.whale_screen.add_widget(whale_scan)
        # if self.current_screen == self.salmon_screen and not self.current_vid_playing:
        #     self.salmon_screen.remove_widget(salmon_noscan)
        #     self.salmon_screen.add_widget(salmon_scan)
        # if self.current_screen == self.penguin_screen and not self.current_vid_playing:
        #     self.penguin_screen.remove_widget(penguin_noscan)
        #     self.penguin_screen.add_widget(penguin_scan)

    def quiz_time(self, animal, arg):
        self.root.remove_widget(self.current_screen)
        if animal == 'whale':
            self.root.add_widget(self.whale_quiz)
            self.current_screen = self.whale_quiz
        elif animal == 'salmon':
            self.root.add_widget(self.salmon_quiz)
            self.current_screen = self.salmon_quiz
        elif animal == 'penguin':
            self.root.add_widget(self.penguin_quiz)
            self.current_screen = self.penguin_quiz

    def show_answer(self, animal, right, arg):
        self.root.remove_widget(self.current_screen)
        if animal == 'whale':
            if right:
                self.root.add_widget(self.whale_right)
                self.current_screen = self.whale_right
            else:
                self.root.add_widget(self.whale_wrong)
                self.current_screen = self.whale_wrong
        elif animal == 'salmon':
            if right:
                self.root.add_widget(self.salmon_right)
                self.current_screen = self.salmon_right
            else:
                self.root.add_widget(self.salmon_wrong)
                self.current_screen = self.salmon_wrong
        elif animal == 'penguin':
            if right:
                self.root.add_widget(self.penguin_right)
                self.current_screen = self.penguin_right
            else:
                self.root.add_widget(self.penguin_wrong)
                self.current_screen = self.penguin_wrong
        self.allow_scan = True

    def WelcomeScreen(self):
        welcome_screen = FloatLayout()
        if KIOSK_MODE == "FOOD":
            welcome_screen.add_widget(Image(source='img/diet.png', pos_hint={'x':0, 'y':0}))
        elif KIOSK_MODE == "THREATS":
            welcome_screen.add_widget(Image(source='img/threats.png', pos_hint={'x':0, 'y':0}))
        elif KIOSK_MODE == "FAMILY":
            welcome_screen.add_widget(Image(source='img/reproduction.png', pos_hint={'x':0, 'y':0}))
        else:
            welcome_screen.add_widget(Label(text='Welcome!', font_size='40pt'))
            welcome_screen.add_widget(icon_welcome_scan)
        return welcome_screen

    def SalmonScreen(self):
        salmon_screen = FloatLayout()
        if KIOSK_MODE == "FAMILY":
            salmon_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['salmon'])
        if KIOSK_MODE == "FOOD":
            salmon_screen.add_widget(Image(source='img/salmon-diet/salmon-diet.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'salmon'))
            salmon_screen.add_widget(test_knowledge_button)
        if KIOSK_MODE == "THREATS":
            salmon_screen.add_widget(Image(source='img/salmon-threats/salmon-threats.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'salmon'))
            salmon_screen.add_widget(test_knowledge_button)
        return salmon_screen

    def WhaleScreen(self):
        whale_screen = FloatLayout()
        if KIOSK_MODE == "THREATS":
            whale_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['whale'])
        if KIOSK_MODE == "FAMILY":
            whale_screen.add_widget(Image(source='img/whale-reproduction/whale-reproduction.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'whale'))
            whale_screen.add_widget(test_knowledge_button)
        if KIOSK_MODE == "FOOD":
            whale_screen.add_widget(Image(source='img/whale-diet/whale-diet.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'whale'))
            whale_screen.add_widget(test_knowledge_button)
        return whale_screen

    def WhaleQuiz(self):
        whale_quiz = FloatLayout()
        if KIOSK_MODE == "FOOD":
            whale_quiz.add_widget(Image(source='img/whale-diet/whale-diet-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/whale-diet/buttons2.png', pos_hint={'x':.14, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/whale-diet/buttons3.png', pos_hint={'x':.32, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/whale-diet/buttons4.png', pos_hint={'x':.5, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/whale-diet/buttons5.png', pos_hint={'x':.68, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'whale', False))
            btn2.bind(on_press=partial(self.show_answer, 'whale', True))
            btn3.bind(on_press=partial(self.show_answer, 'whale', False))
            btn4.bind(on_press=partial(self.show_answer, 'whale', False))
            whale_quiz.add_widget(btn1)
            whale_quiz.add_widget(btn2)
            whale_quiz.add_widget(btn3)
            whale_quiz.add_widget(btn4)
        if KIOSK_MODE == "FAMILY":
            whale_quiz.add_widget(Image(source='img/whale-reproduction/whale-reproduction-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/whale-reproduction/buttons13.png', pos_hint={'x':.14, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/whale-reproduction/buttons14.png', pos_hint={'x':.32, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/whale-reproduction/buttons15.png', pos_hint={'x':.5, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/whale-reproduction/buttons16.png', pos_hint={'x':.68, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'whale', False))
            btn2.bind(on_press=partial(self.show_answer, 'whale', False))
            btn3.bind(on_press=partial(self.show_answer, 'whale', True))
            btn4.bind(on_press=partial(self.show_answer, 'whale', False))
            whale_quiz.add_widget(btn1)
            whale_quiz.add_widget(btn2)
            whale_quiz.add_widget(btn3)
            whale_quiz.add_widget(btn4)
        return whale_quiz

    def SalmonQuiz(self):
        salmon_quiz = FloatLayout()
        if KIOSK_MODE == "FOOD":
            salmon_quiz.add_widget(Image(source='img/salmon-diet/salmon-diet-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/salmon-diet/buttons25.png', pos_hint={'x':.14, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/salmon-diet/buttons26.png', pos_hint={'x':.32, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/salmon-diet/buttons27.png', pos_hint={'x':.5, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/salmon-diet/buttons28.png', pos_hint={'x':.68, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'salmon', False))
            btn2.bind(on_press=partial(self.show_answer, 'salmon', True))
            btn3.bind(on_press=partial(self.show_answer, 'salmon', False))
            btn4.bind(on_press=partial(self.show_answer, 'salmon', False))
            salmon_quiz.add_widget(btn1)
            salmon_quiz.add_widget(btn2)
            salmon_quiz.add_widget(btn3)
            salmon_quiz.add_widget(btn4)
        if KIOSK_MODE == "THREATS":
            salmon_quiz.add_widget(Image(source='img/salmon-threats/salmon-threats-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/salmon-threats/buttons29.png', pos_hint={'x':.14, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/salmon-threats/buttons30.png', pos_hint={'x':.32, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/salmon-threats/buttons31.png', pos_hint={'x':.5, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/salmon-threats/buttons32.png', pos_hint={'x':.68, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'salmon', False))
            btn2.bind(on_press=partial(self.show_answer, 'salmon', False))
            btn3.bind(on_press=partial(self.show_answer, 'salmon', False))
            btn4.bind(on_press=partial(self.show_answer, 'salmon', True))
            salmon_quiz.add_widget(btn1)
            salmon_quiz.add_widget(btn2)
            salmon_quiz.add_widget(btn3)
            salmon_quiz.add_widget(btn4)
        return salmon_quiz

    def PenguinQuiz(self):
        penguin_quiz = FloatLayout()
        if KIOSK_MODE == "FOOD":
            penguin_quiz.add_widget(Image(source='img/penguin-diet/penguin-diet-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/penguin-diet/buttons17.png', pos_hint={'x':.14, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/penguin-diet/buttons18.png', pos_hint={'x':.32, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/penguin-diet/buttons19.png', pos_hint={'x':.5, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/penguin-diet/buttons20.png', pos_hint={'x':.68, 'y':.3}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'penguin', False))
            btn2.bind(on_press=partial(self.show_answer, 'penguin', False))
            btn3.bind(on_press=partial(self.show_answer, 'penguin', True))
            btn4.bind(on_press=partial(self.show_answer, 'penguin', False))
            penguin_quiz.add_widget(btn1)
            penguin_quiz.add_widget(btn2)
            penguin_quiz.add_widget(btn3)
            penguin_quiz.add_widget(btn4)
        if KIOSK_MODE == "THREATS":
            penguin_quiz.add_widget(Image(source='img/penguin-threats/penguin-threats-quiz.png', pos_hint={'x':0, 'y':0}))
            btn1 = Button(background_normal='img/penguin-threats/buttons21.png', pos_hint={'x':.14, 'y':.4}, size_hint=(None, None), size=(293,279))
            btn2 = Button(background_normal='img/penguin-threats/buttons22.png', pos_hint={'x':.32, 'y':.4}, size_hint=(None, None), size=(293,279))
            btn3 = Button(background_normal='img/penguin-threats/buttons23.png', pos_hint={'x':.5, 'y':.4}, size_hint=(None, None), size=(293,279))
            btn4 = Button(background_normal='img/penguin-threats/buttons24.png', pos_hint={'x':.68, 'y':.4}, size_hint=(None, None), size=(293,279))
            btn1.bind(on_press=partial(self.show_answer, 'penguin', True))
            btn2.bind(on_press=partial(self.show_answer, 'penguin', False))
            btn3.bind(on_press=partial(self.show_answer, 'penguin', False))
            btn4.bind(on_press=partial(self.show_answer, 'penguin', False))
            penguin_quiz.add_widget(btn1)
            penguin_quiz.add_widget(btn2)
            penguin_quiz.add_widget(btn3)
            penguin_quiz.add_widget(btn4)
        return penguin_quiz

    def WhaleRight(self):
        whale_right = FloatLayout()
        if KIOSK_MODE == "FOOD":
            whale_right.add_widget(Image(source='img/whale-diet/whale-diet-quiz-right.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "FAMILY":
            whale_right.add_widget(Image(source='img/whale-reproduction/whale-reproduction-quiz2.png', pos_hint={'x':0, 'y':0}))
        return whale_right

    def WhaleWrong(self):
        whale_wrong = FloatLayout()
        if KIOSK_MODE == "FOOD":
            whale_wrong.add_widget(Image(source='img/whale-diet/whale-diet-quiz-wrong.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "FAMILY":
            whale_wrong.add_widget(Image(source='img/whale-reproduction/whale-reproduction-quiz3.png', pos_hint={'x':0, 'y':0}))
        return whale_wrong

    def SalmonRight(self):
        salmon_right = FloatLayout()
        if KIOSK_MODE == "FOOD":
            salmon_right.add_widget(Image(source='img/salmon-diet/salmon-diet-quiz2.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "THREATS":
            salmon_right.add_widget(Image(source='img/salmon-threats/salmon-threats-quiz2.png', pos_hint={'x':0, 'y':0}))
        return salmon_right

    def SalmonWrong(self):
        salmon_wrong = FloatLayout()
        if KIOSK_MODE == "FOOD":
            salmon_wrong.add_widget(Image(source='img/salmon-diet/salmon-diet-quiz3.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "THREATS":
            salmon_wrong.add_widget(Image(source='img/salmon-threats/salmon-threats-quiz3.png', pos_hint={'x':0, 'y':0}))
        return salmon_wrong

    def PenguinRight(self):
        penguin_right = FloatLayout()
        if KIOSK_MODE == "FOOD":
            penguin_right.add_widget(Image(source='img/penguin-diet/penguin-diet-quiz2.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "THREATS":
            penguin_right.add_widget(Image(source='img/penguin-threats/penguin-threats-quiz2.png', pos_hint={'x':0, 'y':0}))
        return penguin_right

    def PenguinWrong(self):
        penguin_wrong = FloatLayout()
        if KIOSK_MODE == "FOOD":
            penguin_wrong.add_widget(Image(source='img/penguin-diet/penguin-diet-quiz3.png', pos_hint={'x':0, 'y':0}))
        if KIOSK_MODE == "THREATS":
            penguin_wrong.add_widget(Image(source='img/penguin-threats/penguin-threats-quiz3.png', pos_hint={'x':0, 'y':0}))
        return penguin_wrong

    def PenguinScreen(self):
        penguin_screen = FloatLayout()
        if KIOSK_MODE == "FAMILY":
            penguin_screen.add_widget(HAS_VIDEO[KIOSK_MODE]['penguin'])
        if KIOSK_MODE == "FOOD":
            penguin_screen.add_widget(Image(source='img/penguin-diet/penguin-diet.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'penguin'))
            penguin_screen.add_widget(test_knowledge_button)
        if KIOSK_MODE == "THREATS":
            penguin_screen.add_widget(Image(source='img/penguin-threats/penguin-threats.png', pos_hint={'x':0, 'y':0}))
            test_knowledge_button = Button(background_normal='img/test-knowledge.png', size_hint=(None, None), size=(293, 254), pos_hint={'x':.83,'y':.05})
            test_knowledge_button.bind(on_press=partial(self.quiz_time, 'penguin'))
            penguin_screen.add_widget(test_knowledge_button)
        return penguin_screen


    def _update_rect(self, instance, value):
    	self.rect.pos = instance.pos
    	self.rect.size = instance.size

if __name__ == '__main__':
    AquariumApp().run()