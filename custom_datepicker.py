from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import BaseDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty, OptionProperty
from datetime import datetime as _dt
from kivymd.theming import ThemableBehavior
import datetime 

Builder.load_string(
'''
<MDLabeltitle2@MDLabel>:
    theme_text_color: 'Custom'
    text_color: 1,1,1,1
    halign: 'center'
    vlighn: 'center'
    fon_style: 'H5'

<MDLabeltitle@MDLabel>
    theme_text_color: 'Primary'
    halign: 'center'
    vlighn: 'center'
    fon_style: 'Caption'   

<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: 'Primary'
        halign: 'center'
        vlighn: 'center'

<AKDatePicker>:
    #size_hint:(0.9, 0.2)
    size_hint: None,None
    size: 
        (dp(302), dp(450))\
        if root.theme_cls.device_orientation == 'portrait'\
        else (dp(450) , dp(350))

    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                #rgba: root.theme_cls.bg_normal
                rgb: C("#e9ebed")
            RoundedRectangle:
                size: self.size 
                pos: self.pos    

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgb: C("#112651")
                RoundedRectangle:
                    size: self.size 
                    pos: self.pos 
                    radius:[(10.0, 10.0), (10.0, 10.0), (0, 0), (0, 0)]

            MDLabeltitle2:
                text: root._day_title
                bold: True

            MDLabeltitle2:
                text: root._month_title
                bold: True

            MDLabeltitle2:
                text: root._year_title
                bold: True


        BoxLayout:
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgb: C("#008094")
                Rectangle:
                    size: self.size 
                    pos: self.pos 

            MDLabeltitle:
                text: 'Día'           

            MDLabeltitle:
                text: 'Mes'

            MDLabeltitle:
                text: 'Año'


        BoxLayout: 
            ScrollView:
                MDBoxLayout:
                    id: day_view
                    orientation: 'vertical'
                    adaptive_height: True           
            ScrollView:
                MDBoxLayout:
                    id: month_view
                    orientation: 'vertical'
                    adaptive_height: True
            ScrollView:
                MDBoxLayout:
                    id: year_view
                    orientation: 'vertical'
                    adaptive_height: True

        BoxLayout:
            size_hint_y: None
            height: dp(70)
            #padding: [dp(10) , 0]
            #spacing: dp(10)
            canvas.before:
                Color:
                    rgb: C("#f3f3f3")
                Rectangle:
                    size: self.size 
                    pos: self.pos

            BoxLayout:    
                orientation: 'vertical' 
                MDLabel:
                    text:"Desde el:"
                    halign: "center"
                    
                
                MDSeparator:
                MDLabel:
                    id: fromDateTextLabel
                    text:"--/--/2021"
                    halign: "center"
                    bold: True
                    #color: (0, 128/255, 148/255, 1)
                    #font_size:"10dp"
                MDSeparator:

            BoxLayout:    
                orientation: 'vertical' 

                GridLayout:
                    cols:2                    
                    MDCheckbox:
                        id:toDateCheckbox
                        size_hint_x:None
                        width:dp(30)
                        on_state:
                            root._updateDateLabels()
                    MDLabel:
                        text:"hasta el:"
                        halign: "center"
                        #color:(17/255, 38/255, 81/255, 1)
                        #font_size:"8dp"
                        #bold: True
               
                MDSeparator:
                MDLabel:
                    id: toDateTextLabel
                    text:"--/--/2021"
                    halign: "center"
                    bold: True
                    #color: (0, 128/255, 148/255, 1)
                    #font_size:"10dp"                    
                MDSeparator:

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: [dp(10) , 0]
            spacing: dp(10)
            canvas.before:
                Color:
                    rgb: C("#112651")

                RoundedRectangle:
                    size: self.size 
                    pos: self.pos
                    radius: [(0.0, 10.0), (0.0, 10.0), (10, 10), (10, 10)]             

            MDFlatButton:
                text: 'Aceptar'
                #disabled: True
                pos_hint: {'center_x': .5 , 'center_y': .5}
                theme_text_color: "Custom"
                text_color: root.theme_cls.primary_color
                on_release: root._choose()

            MDFlatButton:
                text: 'Cancelar'
                pos_hint: {'center_x': .5 , 'center_y': .5}
                on_release: root.cancel()
    
    '''
)


class AKDatePicker(BaseDialog, ThemableBehavior):
    month_type = OptionProperty('string', options=['string', 'int'])
    year_range = ListProperty([2021, 2051])
    _day_title = StringProperty('--')
    _month_title = StringProperty('--')
    _year_title = StringProperty(str(_dt.now().year))

    def __init__(self, callback=None, **kwargs):
        super(AKDatePicker, self).__init__(**kwargs)
        self.day_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
            "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
        self.month_dic = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril', 
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Deciembre'
        }
        

        self.callback = callback
        for x in (range(self.year_range[0], self.year_range[1])):
            self.ids.year_view.add_widget(ButtonBase(text='%d' % x, on_release=self._set_year))
        #for x in (range(1, 13)):
        for k, v in self.month_dic.items():
            if self.month_type == 'string':
                month = v   #self.month_dic[str(x)]
            else:
                month = str(k)

            self.ids.month_view.add_widget(ButtonBase(text=month, on_release=self._set_month))
        for day in (self.day_list):
            self.ids.day_view.add_widget(ButtonBase(text=day, on_release=self._set_day))

    def _updateDateLabels(self):
        month_number = "--"
        
        for k, v in self.month_dic.items():
                if v == self._month_title:
                    month_number = k
                    break     
        if self.ids.toDateCheckbox.active:    
            self.ids.toDateTextLabel.text = f"{self._day_title}/{month_number}/{self._year_title}"
        else:
            self.ids.fromDateTextLabel.text = f"{self._day_title}/{month_number}/{self._year_title}"

    def _set_day(self, instance):
        self._day_title = instance.text
        self._updateDateLabels()

    def _set_month(self, instance):
        self._month_title = instance.text
        self._updateDateLabels()

    def _set_year(self, instance):
        self._year_title = instance.text
        self._updateDateLabels()

    def on_dismiss(self):
        self._day_title = '--'        
        self._month_title = '--'
        self._year_title = '--'
        return

    def _choose(self):
        from_date = None
        to_date =   None
        try:
            try:
                from_date = datetime.date(
                    int(self.ids.fromDateTextLabel.text[6:]),               
                    int(self.ids.fromDateTextLabel.text[3:5]),
                    int(self.ids.fromDateTextLabel.text[:2])               
                )
            except Exception as e:
                pass

            if self.ids.toDateCheckbox.active:
                try:
                    to_date = datetime.date(
                        int(self.ids.toDateTextLabel.text[6:]),               
                        int(self.ids.toDateTextLabel.text[3:5]),
                        int(self.ids.toDateTextLabel.text[:2])
                    )
                except Exception as e:
                    pass    

            self.callback(from_date, to_date)
            self.cancel()
        except Exception as e:
            self.callback(from_date, to_date)
            self.cancel()


    def cancel(self):
        self.dismiss()


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()