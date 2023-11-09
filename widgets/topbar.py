from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class TopBar(BoxLayout):
    pass


Builder.load_string("""
<Gear@ButtonBehavior+Image>:
    size_hint_x: None
    width: self.height
    source: 'assets/gear.png'

<ArrowUp@ButtonBehavior+Image>:
    source: 'assets/arrow_up.png'
    allow_stretch: True
    keep_ratio: False
    
<ArrowDown@ButtonBehavior+Image>:
    source: 'assets/arrow_down.png'
    allow_stretch: True
    keep_ratio: False
    
<TopBar>:
    canvas:
        Color:
            rgba: 0,0,.1,.5
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y: None
    height: 60
    Label:
        size_hint_x: None
        width: self.height*2
        text: "År:"
    Label:
        size_hint_x: None
        width: self.height
        id: year
        text: "{}".format(app.year)
        on_text:
            app.clear_cargo()
            app.year = int(self.text)
            app.nursery.start_soon(app.api.get_db_pallets)
            app.nursery.start_soon(app.api.get_db_trip)
    BoxLayout:
        size_hint_x: None
        width: self.height*1.2
        orientation: "vertical"
        Button:
            text: "+"
            on_release:
                year.text = f"{int(year.text)+1}"
        Button:
            text: "-"
            on_release:
                year.text = f"{int(year.text)-1}"
    Label:
        size_hint_x: None
        width: self.height*2
        text: "Tur:"
    Label:
        size_hint_x: None
        width: self.height
        id: trip
        text: "{}".format(app.trip)
        on_text:
            app.clear_cargo()
            app.trip = int(self.text)
            app.nursery.start_soon(app.api.get_db_pallets)
            app.nursery.start_soon(app.api.get_db_trip)
    BoxLayout:
        size_hint_x: None
        width: self.height*1.2
        orientation: "vertical"
        Button:
            text: "+"
            on_release:
                trip.text = f"{int(trip.text)+1}"
        Button:
            text: "-"
            on_release:
                trip.text = f"{int(trip.text)-1}"
    Widget:
    Gear:
    Button:
        background_color: 0,0,.1,1
        size_hint_x: None
        width: self.texture_size[0]+25
        text: app.time_string
""")
