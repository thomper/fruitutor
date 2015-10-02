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


class Run():
    def __init__(self, lesson):
        self.lesson = lesson
        self.used = []
        self.current = None
        self.input = ''
        self.next()

    def next(self):
        if len(self.used) < self.lesson.lines_per_run:
            self.current = random.choice(self.unused())
            self.used.append(self.current)
            self.input = ''
            return True
        return False

    def input_char(self, char):
        if char == '\b':
            self.input = self.input[:-1]
        elif char in string.printable:
            self.input += char

    def unused(self):
        return tuple(set(self.lesson.lines) - set(self.used))
