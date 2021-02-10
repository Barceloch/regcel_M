from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    RiseInTransition,
    SwapTransition,
)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
#from filebrowser import FileBrowser
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import (
    MDRaisedButton,
    MDRectangleFlatButton,
    MDFloatingActionButton,
    MDIconButton,
)
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDThemePicker, MDTimePicker, MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.list import (
    ILeftBody,
    ILeftBodyTouch,
    IRightBodyTouch,
    OneLineIconListItem,
    OneLineListItem,
)

# internal imports
#import os
#from os.path import sep, expanduser, isdir, dirname
from sqlite3 import Error
from functools import partial
from time import strftime

# local imports
from database import Database
from popups import DeleteWarning
from custom_widgets import TotalsInfoLabel, PanelInfoLabel
from custom_datepicker import AKDatePicker
from custom_layouts import RegistInfo
from tarifa import calcularImporte
import datetime, time

from generate_pdf import generatePdf

# left iconbutton
class ListLeftIconButton(ILeftBodyTouch, MDIconButton):
    pass


# right iconbutton,checkbox,switch
class ListRightIconButton(IRightBodyTouch, MDIconButton):
    pass


# ScreenManager Class
class ScreenManager(ScreenManager):
    pass


# HomeScreen Class
class HomeScreen(Screen):

    def selectWallpaper(self,theme_mode):
        return "assets/images/background.jpg"
        

# RegisterScreen
class RegisterScreen(Screen, Database):
    """
    Admin screen class
    """

    def onStartRegisterScr(self):
        """
        Function to get call everytime register screen starts
        """

        self.populate_recods_data()


    def dateRange(self):
        new_dates = AKDatePicker(callback=self.populate_recods_data)
        new_dates.open()

    def save_record(self):
        """
        Adds layout to add/modify recods
        """
        record_date = self.ids.panelfecha.text.strip()
        record_time = self.ids.panelhora.text.strip()
        lectura = self.ids.input_lectura.text.strip()

        data = (record_date, record_time, lectura)
        conn = self.connect_database("regceldb.db")
        if int(self.ids.panel_layout.update_from_ID):
            c = conn.execute("select * from {}".format("registros"))
            fields = tuple([des[0] for des in c.description][1:])
            if not self.update_database(
                "registros", conn, fields, data, "id", int(self.ids.panel_layout.update_from_ID)
            ):
                Snackbar(text="Error al actualizar!", duration=0.8).show()
            else:                
                self.ids.input_lectura.text = ""
                self.ids.panelConsumo.text = "0"
                self.ids.panelImporte.text = "0.00"
                self.ids.save_regist_Btn.disabled = True
                self.ids.panel_layout.update_from_ID = "0"
                self.populate_recods_data()
                Snackbar(
                    text="Registro actualizado!",
                    duration=0.8,
                ).show()  
        else:
            try:
                if not self.insert_into_database("registros", conn, data):
                    raise Error
                else:           
                    self.ids.input_lectura.text = ""
                    self.ids.panelConsumo.text = "0"
                    self.ids.panelImporte.text = "0.00"
                    self.ids.save_regist_Btn.disabled = True
                    self.populate_recods_data()
                    Snackbar(
                            text="Registro añadido correctamente", duration=0.8
                        ).show()

            except Error:
                # if table doesn't exist
                with open("registros.sql", "r") as table:
                    self.create_table(table.read().format("registros"), conn)
        
        conn.close()
        
    def populate_recods_data(self,
                            from_date=None,
                            to_date=None
                            ):
        """
        Function to populate/refresh the recods list in the manage section
        """
        # --------------Update User info Data List ---------------------#
        fromDate = datetime.date(2021,1,1) if from_date==None else from_date
        toDate = datetime.date.today() if to_date==None else to_date

        self.ids.rv.data = []

        self.ids.panelfecha.text = str(datetime.date.today().strftime("%d/%m/%Y"))
        self.ids.panelhora.text = str(time.strftime("%I:%M %P"))

        try:
            # data may not be present
            data_list_records = self.extractAllData(
                "regceldb.db", "registros", order_by="id"            
            )
            #print(data_list_records) 
            if data_list_records:
                self.ids.panelLecturaAnterior.text = str(data_list_records[-1][3])
            lect = 0
            totalCons = 0
            for each in data_list_records:
                if fromDate <=  datetime.date(int(each[1][6:]), int(each[1][3:5]), int(each[1][:2])) <= toDate:
                    totalCons = totalCons + (each[3]-lect) if lect > 0 else 0
                    lect = each[3] 

                    x = {
                        "record_id": str(each[0]),
                        "record_date": str(each[1]),
                        "record_time": str(each[2]),
                        "lecturaAnterior": str(f'{data_list_records[data_list_records.index(each)-1][3]}' if each[0] > 1 else '--'),
                        "lectura": str(each[3]),
                        "consumo": str(f'{each[3] - data_list_records[data_list_records.index(each)-1][3]}' if each[0] > 1 else '--'),
                    }
                    

                    self.ids.rv.data.append(x)
                self.ids.totalConsumo.text = str(f"{totalCons} kw/h")
                self.ids.totalImporte.text = calcularImporte(totalCons) + " $"

        except (TypeError, Error):
            pass

    def update_regist_info(self, inst):
        """
        Function to update recods
        """
        conn = self.connect_database("regceldb.db")
        data = self.search_from_database(
            "registros", conn, "id", inst.record_id, order_by="id"
        )[0]

        self.ids.panelfecha.text            = str(data[1])
        self.ids.panelhora.text             = str(data[2])
        self.ids.input_lectura.text         = str(data[3])
        self.ids.panelLecturaAnterior.text  = inst.lecturaAnterior

        self.ids.panelConsumo.text = str(int(data[3]) - int(inst.lecturaAnterior))
        self.ids.panelImporte.text = calcularImporte(int(data[3]) - int(inst.lecturaAnterior))

    def generate_records_pdf(self):
        """
        Fetch From Database and generate pdf
        """
        total_details = {
            "consumo_total": self.ids.totalConsumo.text,
            "importe": self.ids.totalImporte.text,
        }

        if self.ids.rv.data:
            generatePdf(total_details, self.ids.rv.data, None)
            Snackbar(text="PDF Generado!", duration=1.5).show()            
        else:
            Snackbar(text="No hay registros!", duration=1.5).show()


    

    
