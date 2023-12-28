from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

class CustomScreen(Screen):
    bg_color = ListProperty([0, 0, 0, 0]) 
class SettingsPopup(Popup):
    def __init__(self, **kwargs):
        super(SettingsPopup, self).__init__(**kwargs)
        self.title = 'Settings'
        self.size_hint = (None, None)
        self.size = (400, 400)

        layout = GridLayout(cols=2)
        colors = [("White", [1, 1, 1, 1]), ("Red", [1, 0, 0, 1]), ("Green", [0, 1, 0, 1]), ("Blue", [0, 0, 1, 1]), ("Yellow", [1, 1, 0, 1])]
        for color_name, color_value in colors:
            btn = Button(text=color_name, on_press=lambda instance, c=color_value: self.change_bg_color(c))
            layout.add_widget(btn)

        self.add_widget(layout)

    def change_bg_color(self, color):
        print("Changing color to:", color)  
        App.get_running_app().change_bg_color(color)
        self.dismiss()
class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Button(text='Start Quiz', on_press=self.start_quiz))
        self.add_widget(Button(text='Settings', on_press=self.settings))
        self.add_widget(Button(text='Quit', on_press=self.quit))
        self.bg_colors = [('white', [1, 1, 1, 1]), ('blue', [0, 0, 1, 1]), ('green', [0, 1, 0, 1])]
        self.bg_color_index = 0

    def start_quiz(self, instance):
        App.get_running_app().screen_manager.current = 'quiz'

    def settings(self, instance):
        settings_popup = SettingsPopup()
        settings_popup.open()

    def change_background_color(self, color):
        for screen in App.get_running_app().screen_manager.screens:
            screen.bg_color = color

    def quit(self, instance):
        App.get_running_app().stop()

class QuizScreen(BoxLayout):
    question_label = ObjectProperty()
    result_label = ObjectProperty()
    answer_buttons = ListProperty()
    current_question_index = NumericProperty(0)
    score = NumericProperty(0)
    time_elapsed = NumericProperty(0)
    questions = ListProperty([
        {"question": "What is 2 + 2?", "answers": ["3", "4", "5"], "correct": "4"},
        {"question": "What is the capital of France?", "answers": ["Paris", "London", "Berlin"], "correct": "Paris"},
        {"question": "Who wrote 1984?", "answers": ["Orwell", "Shakespeare", "Tolkien"], "correct": "Orwell"},
        {"question": "Who is create Quiz app?", "answers": ["Fikree", "Fikree handsome", "Fikree handsome and so cool"], "correct": "Fikree handsome and so cool"}
    ])
    bg_color = ListProperty([0, 0, 0, 0])  # เพิ่ม property นี้

  
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.timer_event = Clock.schedule_interval(self.update_time, 1)
        self.load_question()  # Load the first question immediately

    def update_time(self, dt):
        self.time_elapsed += 1

    def on_current_question_index(self, instance, value):
        if value < len(self.questions):
            self.load_question()
        else:
            self.end_quiz()

    def load_question(self):
        question = self.questions[self.current_question_index]
        self.question_label.text = question['question']
        self.answer_buttons = question['answers']

    def check_answer(self, answer):
        # ตรวจสอบว่ายังอยู่ในขอบเขตของลิสต์คำถามหรือไม่
        if self.current_question_index < len(self.questions):
            correct_answer = self.questions[self.current_question_index]['correct']
            if answer == correct_answer:
                self.score += 1
                self.result_label.text = "Correct!"
            else:
                self.result_label.text = "Incorrect! Try again."

            # ขยับไปยังคำถามถัดไปหรือจบควิซ
            self.current_question_index += 1
            if self.current_question_index >= len(self.questions):
                self.end_quiz()
        else:
            self.end_quiz()
    def end_quiz(self):
        Clock.unschedule(self.timer_event)
        app = App.get_running_app()
        app.show_result(self.score, self.time_elapsed)


class ResultScreen(BoxLayout):
    score_label = ObjectProperty()
    time_label = ObjectProperty()
    bg_color = ListProperty([0, 0, 0, 0])
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
    def update_results(self, score, time):
        self.score_label.text = f"Score: {score}"
        self.time_label.text = f"Time: {time} seconds"

class QuizApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        # Initialize each screen only once
        if not hasattr(self, 'main_menu_screen'):
            self.main_menu_screen = Screen(name='main_menu')
            self.main_menu_screen.add_widget(MainMenuScreen())

        if not hasattr(self, 'quiz_screen'):
            self.quiz_screen = Screen(name='quiz')
            self.quiz_screen.add_widget(QuizScreen())

        if not hasattr(self, 'result_screen'):
            self.result_screen = Screen(name='result')
            self.result_screen.add_widget(ResultScreen())

        # Add screens to the ScreenManager
        self.screen_manager.add_widget(self.main_menu_screen)
        self.screen_manager.add_widget(self.quiz_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager

    def show_result(self, score, time):
        result_screen_widget = self.result_screen.children[0]
        result_screen_widget.update_results(score, time)
        self.screen_manager.current = 'result'
    def change_bg_color(self, color):
        for screen in self.screen_manager.screens:
            screen.bg_color = color    
    def change_bg_color(self, color):
        print("Applying color:", color)  # เพิ่มสำหรับการดีบัก
        for screen in self.screen_manager.screens:
            screen.bg_color = color        

      

if __name__ == '__main__':
    QuizApp().run()
