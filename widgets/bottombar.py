from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock


class RemoveToggle(ToggleButton):
    text = "Fjern\npaller!"
    def on_state(self,*args):
        if self.state == "down":
            App.get_running_app().prod = "-1"
            self.prod_label.text = "Fjern\npaller!"
            self.prod_label.rect_color = 1,0,0,1
            Clock.schedule_once(self.reset_state, 5)
        else:
            App.get_running_app().prod = "0"
            self.prod_label.rect_color = 0, 0, 0, 0
            self.prod_label.text = ""

    def reset_state(self, dt=0):
        self.state = "normal"
        self.prod_label.text = ""
        App.get_running_app().prod = "0"
        self.prod_label.rect_color = 0, 0, 0, 0

class BottomBar(BoxLayout):
    pass

Builder.load_string("""
<BottomBar>:
    holds: None
    label_ti: label_ti
    prod_label: prod_label
    size_hint_y: None
    height: 60
    TextInput:
        font_size: "25sp"
        size_hint_x: 0.2
        id: label_ti
        on_text:
            app.prod = self.text
            prod_label.text = app.search_prod(self.text).get("text","")
    Button:
        size_hint_x: None
        width: self.height
        text: "<"
        background_color: 1,0,0,1
        on_release:
            label_ti.text = ""
    Button:
        size_hint_x: 0.2
        text: "Produkter"
        background_color: 0,.5,0,1
        on_release:
            Factory.ProductsPopup().open()
    Label:
        id: prod_label
        rect_color: 0,0,0,0
        canvas.before:
            Color:
                rgba: self.rect_color
            Rectangle:
                pos: self.pos
                size: self.size
    BoxLayout:
        Label:
            font_size: "30sp"
            canvas.before:
                Color:
                    rgba: 0,.8,1,.8
                Rectangle:
                    size:self.size
                    pos: self.pos
            text: "Last:"
        BoxLayout:
            orientation: "vertical"
            ToggleButton:
                allow_no_selection: False
                group: "hold"
                text: "Øvre"
                on_state:
                    root.holds.sm.current = "upperhold" if self.state == "down" else "lowerhold"
            ToggleButton:
                text: "Nedre"
                allow_no_selection: False
                state: "down"
                group: "hold"
        Button:
            text: "Lag"
            background_color: 0,0,1,1
            on_release:
                root.holds.lowerhold.layer()
                root.holds.upperhold.layer()
        Button:
            background_color: 0,.7,0,1
            text: "Vis fangst"
            on_release:
                Factory.CargoPopup().open()
        RemoveToggle:
            prod_label: prod_label
            background_color: 1,0,0,1
    Button:
        size_hint_x: None
        width: self.height
        text: "+"
        background_color: 1,1,0,1
        on_release:
            root.holds.scale *= 1.1
    Button:
        size_hint_x: None
        width: self.height
        text: "-"
        background_color: 1,1,0,1
        on_release:
            root.holds.scale *= .99
""")