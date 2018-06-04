#!/usr/bin/python
# GNOME Schedule Settings:
#  Command: take-break -a
#  X Application
#  Minutes: */20

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


class KeyboardBoxLayout(BoxLayout):
    def __init__(self, stop_callback, **kwargs):
        super().__init__(**kwargs)
        self.stop_callback = stop_callback
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] in ('enter', 'spacebar'):
            self.stop_callback()

        return True


class AlertApp(App):
    def build(self):
        alert_image = '/usr/local/share/take-break/alert-image.jpg'

        layout = KeyboardBoxLayout(self.stop,
                                   orientation='vertical')
        text = Label(text='Take a break!',
                     font_size=27,
                     color=(1, 0.3, 0.3, 1),
                     size_hint=(1, 0.09),
                     bold=True)
        image = Image(allow_stretch=True,
                      source=alert_image)
        dismiss = Button(text='Dismiss',
                         on_press=self.stop,
                         size_hint=(1, 0.148),
                         font_size=20,
                         background_color=(0, 0, 0, 1))

        layout.add_widget(text)
        layout.add_widget(image)
        layout.add_widget(dismiss)

        Clock.schedule_once(self.stop, 8)

        return layout


app = AlertApp()
app.run()
