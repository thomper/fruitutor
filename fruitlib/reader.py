from .tutor import Lesson

import os

COMMENT_STR = '#'
NUM_FIELDS = 4
FIELD_NAMES = ('filename', 'lines_per_run', 'highlight', 'mcc_highlight')


class BlankLine(Exception):
    # Line doesn't contain a lesson but also isn't malformed
    pass

class InvalidLesson(Exception):
    pass


def read_lessons(filename):
    '''Reads the lesson table and each lesson in the format used by Twidor:

    filename	lines_per_run	highlight	MCC_highlight

    Note that filename must be written as a unix path, it'll be converted to
    the host os format later.

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
            except BlankLine as e:
                pass
            except InvalidLesson as e:
                print(e)


def read_lesson(line):
    fields = lesson_fields(line)
    with open(fields['filename']) as f:
        lines = f.read().split('\n')
    lines = (s.rstrip() for s in lines)
    lines = tuple(empties_removed(lines))
    fields['lines'] = lines
    validate_lesson(fields)
    return Lesson(**fields)


def lesson_fields(line):
    line = comments_stripped(line)
    fields = line.split('\t')
    fields = (field.strip() for field in fields)
    fields = tuple(empties_removed(fields))
    if len(fields) == 0:
        raise BlankLine()
    if len(fields) != NUM_FIELDS:
        raise InvalidLesson('Incorrect number of fields: {}, expected 4'.format(
            len(fields)))
    fields = dict(zip(FIELD_NAMES, fields))
    fields['filename'] = os.path.join(*fields['filename'].split('/'))  
    return field_types_converted(fields)


def validate_lesson(fields):
    lines_per_run = fields['lines_per_run']
    lines = fields['lines']
    if lines_per_run > len(lines):
        raise InvalidLesson('lines_per_run, {}, was greater than number of lines, {}'.format(
            lines_per_run, len(lines)))
    if lines_per_run < 1:
        raise InvalidLesson('lines per run was less then 1: {}'.format(
            lines_per_run))


def comments_stripped(line):
    return line.split(COMMENT_STR)[0].strip()


def empties_removed(seq):
    return (item for item in seq if len(item) > 0)


def field_types_converted(fields):
    try:
        for convert_func in (int_fields_converted, bool_fields_converted):
            fields = convert_func(fields)
    except ValueError as e:
        raise InvalidLesson(e, fields)
    return fields


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
    raise ValueError("Invalid literal for bool type, expected 'y', 'yes', 'n',"\
                     "or 'no': '{}'".format(s))
