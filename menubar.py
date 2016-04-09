from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MenuBar(BoxLayout):
    def exit(self):
        App.get_running_app().stop()

    def mirror(self):
        self.parent.parent.input_display.mirror()

    def lesson(self):
        pass
