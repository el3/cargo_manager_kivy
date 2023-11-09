from kivy.lang import Builder
from kivy.uix.popup import Popup


class ProductsPopup(Popup):
    pass


Builder.load_string("""
<Product@BoxLayout>:
    label: "0"
    text: ""
    group: ""
    Label:
        text: root.label
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

<ProductsRV@RecycleView>:
    viewclass: 'Product'
    data: app.products
    popup: None
    RecycleBoxLayout:
        orientation: "vertical"
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height

<ProductsPopup>:
    title: "Products"
    ProductsRV:
        popup: root
""")
