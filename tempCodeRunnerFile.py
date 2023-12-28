from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

class MainMenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Button(text='Start Quiz', on_press=self.start_quiz))
        self.add_widget(Button(text='Settings', on_press=self.settings))
        self.add_widget(Button(text='Quit', on_press=self.quit))

    def start_quiz(self, instance):
        App.get_running_app().screen_manager.current = 'quiz'

    def settings(self, instance):
        # โลจิกสำหรับการตั้งค่า
        pass

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
        App.get_running_app().end_quiz(self.score, self.time_elapsed)

class ResultScreen(BoxLayout):
    score_label = ObjectProperty()
    time_label = ObjectProperty()

    def update_results(self, score, time):
        self.score_label.text = f"Score: {score}"
        self.time_label.text = f"Time: {time} seconds"

class QuizApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.main_menu_screen = Screen(name='main_menu')
        self.quiz_screen = Screen(name='quiz')
        self.result_screen = Screen(name='result')

        quiz_screen_widget = QuizScreen()
        self.quiz_screen.add_widget(quiz_screen_widget)
        self.result_screen.add_widget(ResultScreen())

        self.screen_manager.add_widget(self.main_menu_screen)
        self.screen_manager.add_widget(self.quiz_screen)
        self.screen_manager.add_widget(self.result_screen)
        self.main_menu_screen.add_widget(MainMenuScreen())
        self.screen_manager.add_widget(self.main_menu_screen)
        # ส่งอ้างอิงไปยัง App ให้ QuizScreen
        quiz_screen_widget.app = self

        return self.screen_manager

    def show_result(self, score, time):
        result_screen_widget = self.result_screen.children[0]
        result_screen_widget.update_results(score, time)
        self.screen_manager.current = 'result'
if __name__ == '__main__':
    QuizApp().run()
