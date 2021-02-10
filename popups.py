from kivy.uix.screenmanager import SwapTransition
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel

from sqlite3 import Error
from time import strftime

from database import Database
from animator.attention import ShakeAnimator


class DeleteWarning(ModalView, Database):
    def __init__(self, id_, data, db_file, table_name, *args, **kwargs):

        self.id_ = id_
        self.data = data
        self.db_file = db_file
        self.table_name = table_name
        self.success = False  # status of deletion
        self.callback = None  # can be called after completion of any action, generally after deletion
        self.delete_detail = ""
        try:
            self.callback = kwargs["callback"]
        except:
            pass

        if self.id_ == "registros":
            self.condition = (
                'record_date = "'
                + data["record_date"]
                + '" AND lectura = "'
                + data["lectura"]
                + '"'
            )
            self.delete_detail = "Lectura: {} \nFecha: {}".format(
                data["lectura"], data["record_date"]
            )

        
        super(DeleteWarning, self).__init__(*args)

    def delete(self, app, text_color):
        """
        code for deleting from database goes here
        """
        conn = self.connect_database(self.db_file)
        res = self.delete_from_database(self.table_name, conn, self.condition)
        conn.close()

        if res:
            if self.id_ == "fee":
                if self.delete_table(
                    self.db_file, self.table_name + "_" + self.data["sem"]
                ):
                    self.success = True
                    res_text = "Eliminado correctamente!"

                    if self.callback is not None:
                        self.callback()

                else:
                    res_text = "Ops!, ha ocurrido un error!"
            else:
                self.success = True
                res_text = "Eliminado correctamente!"

                if self.callback is not None:
                    self.callback()
        else:
            res_text = "Ops!, ha ocurrido un error!"

        self.ids.container.clear_widgets()
        layout = GridLayout(cols=1)
        self.ids.container.add_widget(layout)
        layout.add_widget(
            Label(text=res_text, font_size="25sp") #font_size=self.height / 25 + self.width / 25
        )
        anc_layout = AnchorLayout()
        layout.add_widget(anc_layout)

        raised = MDRaisedButton()
        raised.text = "Ok"
        raised.bind(on_release=self.dismiss)
        raised.md_bg_color = (0, 128/255, 148/255, 1)
        raised.text_color = text_color
        raised.elevation_normal = 10
        anc_layout.add_widget(raised)

    def anim_in(self, instance):
        anim = Animation(pos_hint={"x": 1.4}, t="in_cubic", d=0.3)
        anim.start(instance)

    def anim_out(self, instance):
        anim = Animation(pos_hint={"x": 0.2}, t="out_cubic", d=0.3)
        anim.start(instance)

