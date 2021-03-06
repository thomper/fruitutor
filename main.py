import inputdisplay
from fruitlib import tutor

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

import os


DEFAULT_LESSONS_FILE = os.path.join('lessons', 'lessons.txt')


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


class Main(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_display.on_load()
        self.get_keyboard()
        self.session = tutor.Session(DEFAULT_LESSONS_FILE,
                                     (self.update_user_sentence, ),
                                     (self.on_sentence_complete, ))
        self.update_current_sentence()

    def get_keyboard(self):
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        pass

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        try:
            char = chr(keycode[0])
        except ValueError:
            return  # Super and Menu will cause this
        if char in ('\r', '\n', '\r\n'):
            char = '\n'

        # This shift handling is a temporary hack for testing
        if 'shift' in modifiers:
            char = char.upper()
            if char in SHIFT_KEYS:
                char = SHIFT_KEYS[char]

        self.session.input_char(char)

    def update_current_sentence(self):
        self.tutor_display.lesson_sentence.text = self.session.current_sentence
        self.highlight_keys()

    def update_user_sentence(self, sentence):
        self.tutor_display.user_sentence.text = sentence
        self.highlight_keys()

    def on_sentence_complete(self):
        self.next_sentence()

    def next_sentence(self):
        self.session.next_sentence()
        self.update_current_sentence()

    def highlight_keys(self):
        try:
            self.input_display.highlight_keys(self.session.next_char)
        except AttributeError:
            pass  # this method can be called before self.session is set


class MainApp(App):
    def build(self):
        return Main()


if __name__ == '__main__':
    MainApp().run()
