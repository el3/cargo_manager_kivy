from kivy.lang import Builder
from kivy.uix.popup import Popup

class CargoPopup(Popup):
    pass

Builder.load_string("""
<Cargo@BoxLayout>:
    label: ""
    text: ""
    count: "0"
    group: ""
    Label:
        text: root.count
        size_hint_x: 0.1
        canvas:
            Line:
                rectangle: self.x,self.y,self.width,self.height   
    Button:
        text: root.text
        background_color: app.product_colors.get(root.group) or (.6,.6,.6)
        on_release:
            app.prod = root.label
            app.root.label_ti.text = root.label
            root.parent.parent.popup.dismiss()
    Label:
        text: f"{int(root.count)*720/1000} ton"
        size_hint_x: 0.1
        canvas:
            Line:
                rectangle: self.x,self.y,self.width,self.height   

<CargoPopup>:
    title: "Cargo"
    CargoRV:
        popup: root

<CargoRV@RecycleView>:
    viewclass: 'Cargo'
    data: app.set_catch_view(self)
    popup: None
    RecycleBoxLayout:
        orientation: "vertical"
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
""")