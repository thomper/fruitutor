from tutor import Lesson

import os

COMMENT_STR = '#'
NUM_FIELDS = 4
FIELD_NAMES = ('filename', 'lines_per_run', 'highlight', 'mcc_highlight')


class InvalidLesson(Exception):
    pass


def read_lessons(filename):
    '''Reads the lesson table and each lesson in the format used by Twidor:

    filename	lines_per_run	highlight	MCC_highlight

    Note that there are tabs between each field, not spaces.  Extraneous
    whitespace is stripped.  # begins a comment, everything from there to the
    end of the line is ignored.

    E.g.:

    lesson1.txt	10	y	y
    '''
    with open(filename) as f:
        for line in f:
            try:
                yield read_lesson(line)
            except InvalidLesson as e:
                pass


def read_lesson(line):
    fields = lesson_fields(line)
    with open(fields['filename']) as f:
        lines = f.read().split('\n')
    lines = (s.rstrip() for s in lines)
    lines = tuple(empties_removed(lines))
    fields['lines'] = lines
    if not lesson_is_valid(fields):
        raise InvalidLesson()
    return Lesson(**fields)


def lesson_fields(line):
    line = comments_stripped(line)
    fields = line.split('\t')
    fields = (field.strip() for field in fields)
    fields = tuple(empties_removed(fields))
    if len(fields) != NUM_FIELDS:
        raise InvalidLesson()
    fields = dict(zip(FIELD_NAMES, fields))
    fields = int_fields_converted(fields)
    return bool_fields_converted(fields)


def lesson_is_valid(fields):
    return all((fields['lines_per_run'] <= len(fields['lines']),
                fields['lines_per_run'] >= 1))


def comments_stripped(line):
    return line.split(COMMENT_STR)[0].strip()


def empties_removed(seq):
    return (item for item in seq if len(item) > 0)


def int_fields_converted(fields):
    return applied_to_keyed(fields, ('lines_per_run', ), int)


def bool_fields_converted(fields):
    return applied_to_keyed(fields, ('highlight', 'mcc_highlight'),
                            bool_from_yes_no)


def applied_to_keyed(dct, keys, func):
    dct = dict(dct)  # don't mutate original
    for key in keys:
        dct[key] = func(dct[key])
    return dct


def bool_from_yes_no(s):
    if s.lower() in ('yes', 'y'):
        return True
    elif s.lower() in ('no', 'n'):
        return False
    return None
