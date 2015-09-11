from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout


Builder.load_file('menubar.kv')
Builder.load_file('inputdisplay.kv')
Builder.load_file('tutordisplay.kv')
Builder.load_file('statsdisplay.kv')


class Fruitutor(FloatLayout):
    pass


class FruitutorApp(App):
    def build(self):
        return Fruitutor()


if __name__ == '__main__':
    FruitutorApp().run()
