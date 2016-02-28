import fruitlib.reader

import string
import random


class Lesson():
    def __init__(self, filename, lines_per_run, highlight, mcc_highlight,
                 lines):
        self.filename = filename
        self.lines_per_run = lines_per_run
        self.highlight = highlight
        self.mcc_highlight = mcc_highlight
        self.lines = lines

    def __str__(self):
        return '''Lesson:
Filename: {}
Lines per run: {}
Highlight: {}
Highlight MCC: {}
Lines: {}'''.format(self.filename,
             self.lines_per_run,
             self.highlight,
             self.mcc_highlight,
             len(self.lines))


class LessonRun():
    def __init__(self, lesson, input_callbacks=None, sentence_callbacks=None):
        self.lesson = lesson
        self.input_callbacks = input_callbacks or ()
        self.sentence_callbacks = sentence_callbacks or ()
        self.used = []
        self.current = None
        self.input = ''
        self.next()

    def next(self):
        if len(self.used) < self.lesson.lines_per_run:
            self.change_sentence(random.choice(self.unused()))
            return True
        return False

    def input_char(self, char):
        if char == '\b':
            self.input = self.input[:-1]
        elif char == '\n':
                self.check_sentence_complete()
        elif not (type(char) == str and len(char) == 1):
            return
        elif char in string.printable:
            if len(self.input) < len(self.current):
                self.input += char
        self.do_input_callbacks()
        # TODO: stats

    def check_sentence_complete(self):
        if self.input.lower() == self.current.lower():
            self.do_sentence_callbacks()

    def unused(self):
        return tuple(set(self.lesson.lines) - set(self.used))

    def change_sentence(self, sentence):
        self.current = sentence
        self.used.append(self.current)
        self.clear_input()

    def clear_input(self):
        self.input = ''
        self.do_input_callbacks()

    def do_input_callbacks(self):
        for cb in self.input_callbacks:
            cb(self.input)

    def do_sentence_callbacks(self):
        for cb in self.sentence_callbacks:
            cb()


class Session():
    def __init__(self, lessons_file, input_callbacks, sentence_callbacks):
        self.lessons = tuple((Lesson(**fields) for fields in
                              fruitlib.reader.read_lessons(lessons_file)))
        self.input_callbacks = input_callbacks or ()
        self.sentence_callbacks = sentence_callbacks or ()
        self.current_lesson = 0
        self.run = None
        self.load_lesson()

    @property
    def current_sentence(self):
        return self.run.current

    def input_char(self, char):
        self.run.input_char(char)

    def load_lesson(self):
        self.run = LessonRun(self.lessons[self.current_lesson],
                             self.input_callbacks, self.sentence_callbacks)

    def next_sentence(self):
        if self.run.next():
            return True
        else:
            return self.next_lesson()

    def next_lesson(self):
        if self.current_lesson + 1 >= len(self.lessons):
            return False
        else:
            self.current_lesson += 1
            self.run.input = ''  # old Run updates input display again after new run is created
            self.load_lesson()
