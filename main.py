# -*- coding: UTF-8 -*-
"""
	Algo
"""

# minimal main file
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window, WindowBase
from kivy.config import Config
import json

from kivymd.uix.dialog import  MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.theming import ThemeManager
from kivy.utils import platform, get_hex_from_color

from sqlite3 import Error
from database import Database
from screens import HomeScreen
from custom_about import AboutDialog

Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set('graphics', 'resizable', 1)

#if platform != 'android':
#    Window.size = (330, 650)




# Main App
class RegCElSystem(MDApp, Database):
    dialog = None 
    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Light"
        super().__init__(**kwargs)

    def on_start(self):
        Window.set_title("RegCEl M_v0.1")
       
    def build(self):
        return Builder.load_file("gui.kv")

    def about(self):
        _about = AboutDialog()
        _about.open()    

    def confirmCloseDialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Seguro que desea salir?",
                buttons=[
                    MDFlatButton(
                        text="Sí", 
                        on_release=lambda _:self.stop()
                    ),
                    MDFlatButton(
                        text="No", 
                        on_release=lambda _: self.dialog.dismiss()
                    ),
                ],
                )

        self.dialog.open()

if __name__ == "__main__":
    #Window.size = (360, 600)
    Window.size = (330, 650)
    RegCElSystem().run()
