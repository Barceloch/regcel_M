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

Builder.load_string(
'''
<ButtonBase>
    size_hint_y: None
    height: dp(40)
    MDLabel:
        id: value
        text: root.text
        theme_text_color: 'Primary'
        halign: 'center'
        vlighn: 'center'

<AboutDialog>:
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

            MDLabeltitle:
                theme_text_color: 'Custom'
                text_color: 1,1,1,1
                halign: 'center'
                vlighn: 'center'
                fon_style: 'H5'  
                text: "Acerca de..."
                bold: True

        BoxLayout:
            ScrollView:
                MDBoxLayout:
                    RstDocument:
                        source: 'about.rst'


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


class AboutDialog(BaseDialog, ThemableBehavior):
    def cancel(self):
        self.dismiss()


class ButtonBase(RectangularRippleBehavior, ButtonBehavior, BoxLayout):
    text = StringProperty()