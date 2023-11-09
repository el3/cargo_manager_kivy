import os, sys
if not sys.stderr:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

if getattr(sys, 'frozen', False):
    from kivy.resources import resource_add_path
    resource_add_path(sys._MEIPASS)

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.core.window import Window

import widgets
import db
from data.products import products, product_colors

from datetime import datetime, timedelta
from collections import Counter
import trio
from functools import partial


KV = '''
#:import Factory kivy.factory.Factory
#:import NoTransition kivy.uix.screenmanager.NoTransition

<ScreenManager>:
    transition: NoTransition()

<Label>:
    font_size: "20sp"

<DataLabel@Label>:
    color: .7,0,0,.8
    canvas:
        Color:
            rgba: 1,0,0,.5
        Line:
            rectangle: self.x,self.y,self.width,self.height

FloatLayout:
    label_ti: bottombar.label_ti
    prod_label: bottombar.prod_label
    holds: [holds.lowerhold,holds.upperhold]
    Holds:
        pos: mainarea.pos
        size: mainarea.size
        id: holds
    BoxLayout:
        orientation: "vertical"
        TopBar:
        RelativeLayout:
            id: mainarea
            BoxLayout:
                orientation: "vertical"
                size_hint: 0.15,0.2
                padding: 5
                spacing: 5
                pos_hint: {"right":1,"top":1}
                DataLabel:
                    text: f"{len(app.cargo)*720/1000} ton i last"
                    color: 0,.7,0,.8
                DataLabel:
                    text: f"{len(app.cargo)} paller i last"
                    color: 0,.7,0,.8
                DataLabel:
                    text: f"{(1748*720-len(app.cargo)*720)/1000} ton tilbage"
                DataLabel:
                    text: f"{1748-len(app.cargo)} paller tilbage"
        BottomBar:
            id: bottombar
            holds: holds
'''

class CargoApp(App):
    title = "Cargo"
    prod = StringProperty("")
    time_string = StringProperty("")
    time = datetime.utcnow()
    trip = NumericProperty(1)
    year = NumericProperty(2023)

    products = products
    product_colors = product_colors

    cargo = ListProperty([])

    # "http://0.0.0.0:8080/api/"
    api = db.Api("http://192.168.1.10/api/")

    async def async_run(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery
            await super().async_run('trio')
            nursery.cancel_scope.cancel()

    def search_prod(self, label):
        data = [item for item in self.products if item.get('label') == label]
        if len(data):
            return data[0]
        else:
            return {}

    def build(self):
        Window.maximize()
        self.update_time()
        Clock.schedule_interval(self.update_time,10)
        Clock.schedule_once(partial(self.nursery.start_soon, self.api.get_db_pallets),.5)
        Clock.schedule_interval(partial(self.nursery.start_soon, self.api.get_db_pallets), 5)
        return Builder.load_string(KV)

    def update_time(self,dt=0):
        self.time = datetime.utcnow()
        self.time_string = self.time.strftime('%Y-%m-%d %H:%M')

    def set_pallets(self,data,hold,space,_datetime,label,layer,_id,dt=0):
        space = self.root.holds[hold].children[space]
        space.add_pallet(data,space.children[layer],_datetime,label,_id)

    def clear_cargo(self):
        for hold in [0,1]:
            for space in self.root.holds[hold].children:
                space.clear_pallet()
                space.clear_pallet()

    def set_catch_view(self,rv):
        print(self.cargo)
        labels = [i.get("label") for i in self.cargo]
        count_dict = dict(Counter(labels))
        data = [{"text": self.search_prod(str(key)).get("text", ""),
                 "count":str(val),"group":self.search_prod(str(key)).get("group", ""),
                 "label":str(key)} for key,val in count_dict.items()]
        rv.data = data
        return data

if __name__ == '__main__':
    app = CargoApp()
    trio.run(app.async_run)