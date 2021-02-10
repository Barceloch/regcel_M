from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.uix.screenmanager import RiseInTransition
from kivy.utils import get_color_from_hex as C
from kivy.factory import Factory

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.snackbar import Snackbar

from database import Database
from hoverable import HoverBehavior
from custom_widgets import LabelForList
from popups import DeleteWarning

import os
from kivy.utils import platform
from os.path import sep, expanduser, isdir, dirname
from functools import partial

# Being used in Manage Student section
class HoverLayout(BoxLayout, HoverBehavior):
    pass


class RegistInfo(BoxLayout, Database):
    def delete(self, app, root):
        fields = [ch.children[0].text
                    for child in root.children[-2:0:-1]
                    for ch in child.children]
     
        data = {"record_date": fields[1], "record_time": fields[0], "lectura": fields[3]}

        
        DeleteWarning(
            "registros",
            data,
            "regceldb.db",
            "registros",
            callback=app.root.ids.registerScreen.populate_recods_data,
        ).open()
        

class AddRegistLayout(FloatLayout):
    def manage_icon(self, btn):
        date = self.ids.name.text
        time = self.ids.email.text
        lectura = self.ids.username.text

        data = [date, time, lectura]

        if any([len(each) for each in data]):
            btn.icon = "check"
        elif not btn.icon == "plus":
            btn.icon = "window-close"

