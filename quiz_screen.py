from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label 

class QuizScreen(BoxLayout):
    question_label = ObjectProperty()
    result_label = ObjectProperty()
    answer_buttons = ListProperty()
    current_question_index = NumericProperty(0)
    score = NumericProperty(0)
    time_elapsed = NumericProperty(0)
    questions = ListProperty([
        {"question": "What is 2 + 2?", "answers": ["3", "4", "5"], "correct": "4"},
        {"question": "What is the capital of France?", "answers": ["Paris", "London", "Berlin"], "correct": "Paris"}
    ])
    bg_color = ListProperty([0, 0, 0, 0])  # เพิ่ม property นี้
    def on_questions(self, instance, value):
        # รีเซ็ตคำถามเมื่อมีการเปลี่ยนแปลงรายการคำถาม
        self.current_question_index = 0
        self.load_question()
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
    custom_message_label = ObjectProperty()  # Add a new label for custom message
    bg_color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        # Add the custom message label to the layout
        self.custom_message_label = Label()
        self.add_widget(self.custom_message_label)

    def update_results(self, score, time):
        self.score_label.text = f"Score: {score}"
        self.time_label.text = f"Time: {time} seconds"
        # Update the custom message based on the score
        if score >= 5:
            self.custom_message_label.text = "Great job!"

        else:
            self.custom_message_label.text = "Needs improvement!"
