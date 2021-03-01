#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
# PROJECT   : RegCEl - Registro para el Consumo Eléctrico                                              #
# VERSION   : 1.2                                                                                                      #
# AUTHOR    : Yunior Barceló Chávez             barceloch@gmail.com                                                                         #
# DATE      : 9/01/2021                                                                                               #
#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-#
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import BaseDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.theming import ThemableBehavior
from kivy.app import App

Builder.load_string(
'''
<MDCheckbox>
    canvas:
        Clear
        Color:
            rgba: root.theme_cls.primary_color
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos:
                int(self.center_x - self.texture_size[0] / 2.),\
                int(self.center_y - self.texture_size[1] / 2.)

    color: self._current_color
    halign: 'center'
    valign: 'middle'

<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: 'Primary'
        halign: 'center'
        vlighn: 'center'

<ContribDialog>:
    #size_hint:(0.9, 0.2)
    size_hint: None,None
    size:(dp(300), dp(460))

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

            MDLabel:
                theme_text_color: 'Custom'
                text_color: 1,1,1,1
                halign: 'center'
                vlighn: 'center'
                fon_style: 'H5'  
                text: "Contribuir!"
                bold: True

        BoxLayout:
            size_hint_y: None
            height: dp(120)
            ScrollView:
                MDBoxLayout:
                    RstDocument:
                        text: "Una vez obtenida esta app, usted puede compartirla libremente con sus amistades haciéndola más accesible a todos. Si le resulta útil y desea contribuir con el desarrollo de nuevas versiones para incluir otras funcionalidades, haciendo una donación en CUP, puede usar la tarjeta y el móvil especificados o escaneando el código Qr; será de gran ayuda. Gracias!"      
          
        GridLayout:
            #orientation: 'vertical'            
            padding: dp(1)
            spacing: dp(8)
            rows: 2
            BoxLayout:
                size_hint: 1, None
                height: dp(25)
                #spacing: dp(50)
                #padding: dp(-10)
                canvas:
                    Color:
                        rgb: C("#008094")
                    Rectangle:
                        size: self.size 
                        pos: self.pos 
        #        MDCheckbox:
        #            id: transferm
        #            size_hint: (0.3,1)
        #            group: "qrcode"
        #            active: True
        #            disabled:True
        #            on_state:
        #                self.disabled=True
        #                root.ids.enzona.disabled=False 
        #                root.ids.qrcode.icon = "assets/images/transfermovilqr.jpg"                     
                MDLabel:
                    #pos_hint: {"center_x": 100, "center_y": .5}
                    theme_text_color: 'Custom'
                    text: "9224-0699-9137-5144 | +53 53592879"
                    text_color: (17/255, 38/255, 81/255, 1)
                    bold:True

        #        MDCheckbox:
        #            id: enzona
        #            size_hint: (0.3,1)
        #            group: "qrcode"
        #            on_state:
        #                self.disabled=True 
        #                root.ids.transferm.disabled=False
        #                root.ids.qrcode.icon = "assets/images/enzonaqr.jpg"     
        #        MDLabel:
        #            theme_text_color: 'Custom'
        #            text: "Enzona"
        #            text_color: (17/255, 38/255, 81/255, 1)
        #            bold:True
            AnchorLayout:
                MDFloatingActionButton:                
                    id: qrcode
                    size_hint: None, None
                    size: dp(220), dp(220)                
                    haling:"center"
                    icon: "assets/images/transfermovilqr.png"
                    elevation_normal: 0                
                    readonly: True

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
                text: 'Salir'
                #disabled: True
                pos_hint: {'center_x': .5 , 'center_y': .5}
                theme_text_color: "Custom"
                text_color: root.theme_cls.primary_color
                on_release: root.cancel()
    
    '''
)


class ContribDialog(BaseDialog, ThemableBehavior):
    def close(self):
        app= App.get_running_app()
        app.stop()

    def cancel(self):
        self.dismiss()    


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()