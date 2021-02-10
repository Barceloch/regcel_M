"""
This file contains different customized widgets

Availabe classes:
-----------------
    - HoverOneLineListItem
    - LabelForList
    - LabelForListStudent
    - AdminInfoLabel
    - AdminInfoEditField
    - CustomRecycleView

"""

from kivymd.uix.list import OneLineListItem
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView

from hoverable import HoverBehavior





class LabelForList(Label):
    """
    This class creates universal label to be used in list items across this application
    """

    pass

class TotalsInfoLabel(BoxLayout):
    """
    Customized `Label` to show personal/credential informations of the admin
    """

    pass

class PanelInfoLabel(BoxLayout):
    """
    Customized `Label` to show personal/credential informations of the admin
    """

    pass


