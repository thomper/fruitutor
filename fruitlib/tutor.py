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
