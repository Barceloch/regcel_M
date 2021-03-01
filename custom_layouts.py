#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
# PROJECT   : RegCEl - Registro para el Consumo Eléctrico                                              #
# VERSION   : 1.2                                                                                                      #
# AUTHOR    : Yunior Barceló Chávez             barceloch@gmail.com                                                                         #
# DATE      : 9/01/2021                                                                                               #
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from database import Database
from hoverable import HoverBehavior
from popups import DeleteWarning

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

