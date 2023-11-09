from kivy.uix.label import Label
from kivy.properties import ListProperty, NumericProperty
from kivy.lang import Builder


class Pallet(Label):
    db_id = NumericProperty(-1)
    color2 = ListProperty([0, 0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(touch.x + self.offset, touch.y - self.offset):
            if self.active:
                self.parent.press(self.text)
                return True
            else:
                return False


Builder.load_string("""
<Pallet>:
    active: False
    size_hint: None, None
    size: 60,40
    offset: 12
    name: ""
    alpha: 0
    color2: [0,0,0]
    color: 0,0,0,self.alpha or 0
    text_size: 60,40
    halign: 'left'
    valign: 'top'
    canvas.before:
        Color:
            rgb: [(i or 0)*0.2 for i in root.color2]
            a: root.alpha
        Mesh:
            mode: "triangle_fan"
            vertices: [self.x, self.y,0,0,\
                        self.x+self.width, self.y,0,0,\
                        self.x-self.offset, self.y+self.offset,0,0,\
                        self.x-self.offset+self.width, self.y+self.offset,0,0]
            indices: [0,2,3,1]
        Color:
            rgb: [(i or 0)*0.3 for i in root.color2]
            a: root.alpha
        Mesh:
            mode: "triangle_fan"
            vertices: [self.x+self.width, self.y,0,0,\
                        self.x+self.width, self.y+self.height,0,0,\
                        self.x+self.width-self.offset, self.y+self.offset,0,0,\
                        self.x+self.width-self.offset, self.y+self.offset+self.height,0,0]
            indices: [0,2,3,1]
        Color:
            rgb: [(i or 0)*0.5 for i in root.color2]
            a: root.alpha
        Rectangle:
            pos: self.x-self.offset, self.y+self.offset
            size: self.size
""")
