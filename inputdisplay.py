from kivy.uix.gridlayout import GridLayout
import util

import itertools


YELLOW = [1, 1, 0.2, 1]
WHITE = [1, 1, 1, 1]
DEFAULT_KEYS = {'a': ('a', ),
                'b': ('b', ),
                'c': ('c', ),
                'd': ('d', ),
                'e': ('e', ),
                'f': ('f', ),
                'g': ('g', ),
                'h': ('h', ),
                'i': ('space', 'b'),
                'j': ('space', 'c'),
                'k': ('space', 'd'),
                'l': ('space', 'f'),
                'm': ('space', 'g'),
                'n': ('space', 'h'),
                'o': ('space', 'delete'),
                'p': ('space', 'backspace'),
                'q': ('space', 'enter'),
                'r': ('e', 'b'),
                's': ('e', 'c'),
                't': ('e', 'd'),
                'u': ('e', 'f'),
                'v': ('e', 'g'),
                'w': ('e', 'h'),
                'x': ('e', 'delete'),
                'y': ('e', 'backspace'),
                'z': ('e', 'enter'),
                '.': ('a', 'b'),
                ',': ('a', 'c'),
                ':': ('a', 'd'),
                "'": ('a', 'f'),
                '"': ('a', 'g'),
                '?': ('a', 'delete'),
                '!': ('a', 'backspace'),
                '-': ('a', 'enter'),
                'space': ('space', ),
                'delete': ('delete', ),
                'backspace': ('backspace', ),
                'enter': ('enter', )}

def highlight(label):
    label.bold = True
    label.color = YELLOW

def unhighlight(label):
    label.bold = False
    label.color = WHITE

class InputDisplay(GridLayout):
    def on_load(self):
        self.keys = DEFAULT_KEYS
        self.labels = {label_name[10:]: self.ids[label_name] for
                       label_name in self.ids if label_name[:10] == 'label_key_'}

    def highlight_keys(self, str_):
        str_ = str_ or ''
        str_ = str_.lower()
        str_ = {' ': 'space', '\b': 'backspace', '\n': 'enter'}.get(str_, str_)
        to_highlight = self.keys.get(str_, ())
        for label_name in self.labels:
            if label_name in to_highlight:
                highlight(self.labels[label_name])
            else:
                unhighlight(self.labels[label_name])

    def mirror(self):
        old_children = tuple(reversed(self.children))  # self.children is in reverse layout order
        for child in old_children:
            self.remove_widget(child)
        old_layout = util.reshape_1d_to_2d(old_children, 3)  # TODO: twiddler layout is 4 rows of 3 keys, do we want to generalise for other keyboards?
        new_layout = (reversed(row) for row in old_layout)
        new_children = itertools.chain(*new_layout)
        for child in new_children:
            self.add_widget(child)
