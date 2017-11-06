from kivy.app import App
from kivy.uix.button import Button

class SimplexApp(App):

    def build(self):
        return Button(text="SIMPLEX")

if __name__ == '__main__':
    SimplexApp().run()
