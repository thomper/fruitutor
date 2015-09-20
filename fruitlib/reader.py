COMMENT_STR = '#'
NUM_FIELDS = 4
FIELD_NAMES = ('filename', 'lines_per_run', 'highlight', 'mcc_highlight')


class InvalidLesson(Exception):
    pass


def read_lessons(filename):
    '''Reads the lesson table and each lesson in the format used by Twidor:

    filename	lines_per_run	highlighting	MCC_highlighting

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
    lesson = get_fields(line)
    with open(lesson['filename']) as f:
        sentences = f.read().split('\n')
    sentences = (s.rstrip() for s in sentences)
    sentences = tuple(empties_removed(sentences))
    lesson['sentences'] = sentences
    return lesson


def get_fields(line):
    line = strip_comments(line)
    fields = line.split('\t')
    fields = (field.strip() for field in fields)
    fields = tuple(empties_removed(fields))
    if len(fields) != NUM_FIELDS:
        raise InvalidLesson()
    return dict(zip(FIELD_NAMES, fields))


def strip_comments(line):
    return line.split(COMMENT_STR)[0].strip()


def empties_removed(seq):
    return (item for item in seq if len(item) > 0)
