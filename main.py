from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty

class QuizScreen(BoxLayout):
    question_label = ObjectProperty()
    result_label = ObjectProperty()
    answer_buttons = ListProperty()
    current_question_index = 0
    questions = ListProperty([
        {"question": "What is 2 + 2?", "answers": ["3", "4", "5"]},
        {"question": "What is the capital of France?", "answers": ["Paris", "London", "Berlin"]},
        {"question": "Who wrote 1984?", "answers": ["Orwell", "Shakespeare", "Tolkien"]}
    ])

    def on_questions(self, instance, value):
        if value:
            self.load_question()

    def load_question(self):
        # ตรวจสอบว่ายังมีคำถามในลิสต์
        if self.current_question_index < len(self.questions):
            self.question_label.text = self.questions[self.current_question_index]['question']
            self.answer_buttons = self.questions[self.current_question_index]['answers']
        else:
            self.answer_buttons = ["", "", ""]
    def check_answer(self, answer):
        correct_answer = self.questions[self.current_question_index]['answers'][1]
        if answer == correct_answer:
            self.result_label.text = 'Correct!'
            self.current_question_index += 1
            if self.current_question_index < len(self.questions):
                self.load_question()
            else:
                self.result_label.text = 'Quiz Completed!'
        else:
            self.result_label.text = 'Incorrect! Try again.'

class QuizApp(App):
    def build(self):
        screen = QuizScreen()
        screen.load_question()  # Load the first question immediately
        return screen

if __name__ == '__main__':
    QuizApp().run()
