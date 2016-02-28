from fruitlib import tutor, reader

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from os import path


Builder.load_file('menubar.kv')
Builder.load_file('inputdisplay.kv')
Builder.load_file('tutordisplay.kv')
Builder.load_file('statsdisplay.kv')


# TODO: actual key depends on system keymap, this is a temporary hack for testing
SHIFT_KEYS = {'`': '~',
              '1': '!',
              '2': '@',
              '3': '#',
              '4': '$',
              '5': '%',
              '6': '^',
              '7': '&',
              '8': '*',
              '9': '(',
              '0': ')',
              '-': '_',
              '=': '+',
              '\\': '|',
              '[': '{',
              ']': '}',
              ';': ':',
              "'": '"',
              ',': '<',
              '.': '>',
              '/': '?'}


class Fruitutor(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lessons = tuple(reader.read_lessons(path.join('lessons', 'lessons.txt')))
        self.run = None
        self.load_lesson()
        self.get_keyboard()

    def get_keyboard(self):
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        pass

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        char = chr(keycode[0])
        if char in ('\r', '\n', '\r\n'):
            char = '\n'

        # This shift handling is a temporary hack for testing
        if 'shift' in modifiers:
            if char.islower():
                char = char.upper()
            elif char in SHIFT_KEYS:
                char = SHIFT_KEYS[char]

        self.run.input_char(char)

    def load_lesson(self):
        self.run = tutor.LessonRun(self.lessons[0], (self.update_user_sentence, ),
                                   (self.on_sentence_complete, ))
        self.update_current_sentence()

    def update_current_sentence(self):
        self.tutor_display.lesson_sentence.text = self.run.current

    def update_user_sentence(self, char, sentence):
        self.tutor_display.user_sentence.text = sentence

    def on_sentence_complete(self):
        self.next_sentence()

    def next_sentence(self):
        if self.run.next():
            self.update_current_sentence()



class FruitutorApp(App):
    def build(self):
        return Fruitutor()


if __name__ == '__main__':
    FruitutorApp().run()
