from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class QuizScreen(BoxLayout):
    def check_answer(self, instance):
        result_label = self.ids['result_label']
        if instance.text == '2':
            result_label.text = 'Good'
        else:
            result_label.text = 'Bad Try agin'

class QuizApp(App):
    def build(self):
        return QuizScreen()

if __name__ == '__main__':
    QuizApp().run()
