from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MenuBar(BoxLayout):
    def exit(self):
        App.get_running_app().stop()

    def mirror(self):
        pass

    def lesson(self):
        pass
