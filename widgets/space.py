from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock

from widgets import Pallet

from datetime import datetime

class Space(ButtonBehavior,RelativeLayout):

    def on_press(self):
        self.press("")
        print((self.x-3)/ 1.03, (self.y+32) / 1.03)

    def clear_pallet(self):
        app = App.get_running_app()
        spaces = [i for i in self.children.__reversed__() if i.active]
        if len(spaces):
            pallet = spaces[-1]
        else:
            return False
        pallet.color2 = (0, 0, 0)
        pallet.text = ""
        pallet.name = ""
        pallet.alpha = 0
        db_id = pallet.db_id
        pallet.db_id = -1
        pallet.active = False
        return pallet, db_id

    def delete_pallet(self):
        app = App.get_running_app()
        clear_pallet = self.clear_pallet()
        if clear_pallet:
            pallet,db_id = clear_pallet
            app.nursery.start_soon(app.api.delete_db_pallet,db_id)


    def add_pallet(self,data,pallet=False,time=False,text=False,db_id=-1):
        app = App.get_running_app()
        color = app.product_colors.get(data.get("group"))
        if not pallet:
            pallet = [i for i in self.children.__reversed__() if not i.active][0]
            pallet.text = app.prod
            pallet.time = datetime.utcnow().isoformat()
            app.nursery.start_soon(app.api.add_db_pallet,pallet.time, pallet.text,
                              self.parent.hold,
                              self.parent.children.index(self),
                              self.children.index(pallet))
        else:
            pallet.time = time
            pallet.text = str(text)
            pallet.db_id = db_id
        pallet.alpha = 1
        pallet.color2 = color
        pallet.name = data.get("text", "")
        pallet.active = True

    def press(self,pallet_text):
        app = App.get_running_app()
        if app.prod == "-1":
            self.delete_pallet()
            return
        data = app.search_prod(app.prod)
        if len(data):
            print([i for i in self.children if i.active])
            if len([i for i in self.children if i.active]) < 2:
                self.add_pallet(data)
                return
            else:
                self.children[0].alpha = .2
                Clock.schedule_once(self.reset,.5)
        app.root.prod_label.text = app.search_prod(pallet_text).get("text","")
        app.root.label_ti.text = app.search_prod(pallet_text).get("label","")

    def reset(self,dt):
        self.children[0].alpha = 1
        print("reset")

    def _add_pallet(self,layer):
        p = Pallet(x=-layer*14,y=layer*14)
        self.add_widget(p)

Builder.load_string("""
<Space>:
    size_hint: None, None
    size: 60,40
    text: ""
    canvas.before:
        Color:
            rgba: 1,1,1,.1
        Rectangle:
            size: self.size
""")