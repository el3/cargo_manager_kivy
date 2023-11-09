from kivy.app import App
from kivy.clock import Clock
import httpx
from functools import partial


class Api:

    def __init__(self, base_url):
        self.base_url = base_url

    async def add_db_pallet(self, dt, label, hold, space, layer):
        app = App.get_running_app()
        # POST Request (Add a Pallet)
        data = {
            'datetime': dt,
            'year': app.year,
            'trip': app.trip,
            'label': label,
            'hold': hold,
            'space': space,
            'layer': layer
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}pallets", json=data)
                if response:
                    print("add_pallet POST response:", response.json())
        except httpx.ConnectError:
            print("Failed to connect to the server.")

    async def delete_db_pallet(self, db_id):
        app = App.get_running_app()
        # DELETE Request (Delete a Pallet)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{self.base_url}pallets/{db_id}")
                if response:
                    print("delete_pallet POST response:", response)
        except httpx.ConnectError:
            print("Failed to connect to the server.")

    async def get_db_pallets(self, dt=0):
        app = App.get_running_app()
        # GET Request (Retrieve Pallets)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}pallets/{app.year}/{app.trip}")
                if response:
                    print("get pallets GET response:", response)
                    resp = response.json().get("pallets", [])
                    app.cargo = resp
                    for row in resp:
                        # [{'datetime': 'Thu, 02 Nov 2023 13:45:32 GMT', 'hold': 0, 'id': 1, 'label': 293, 'layer': 1, 'space': 103, 'trip': 1}]
                        _id = row['id']
                        _datetime = row['datetime']
                        hold = row['hold']
                        space = row['space']
                        layer = row['layer']
                        label = row['label']
                        data = app.search_prod(str(label))
                        Clock.schedule_once(partial(app.set_pallets, data, hold, space, _datetime, label, layer, _id))
                else:
                    return
        except Exception as e:
            print(e)

    async def get_db_trip(self, dt=0):
        app = App.get_running_app()
        # GET Request (Retrieve Pallets)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}trips/{app.year}/{app.trip}")
                if response:
                    print("get trip GET response:", response)
                    resp = response.json().get("trips", [])
                    if len(resp):
                        row = resp[0]
                        print(resp)
                        _id = row['id']
                        year = row['year']
                        trip = row['trip']
                        started = row['started']
                        finished = row['finished']
                        active = row['active']
                    else:
                        app.nursery.start_soon(self.add_db_trip, app.year, app.trip)
                else:
                    print("No response")
        except Exception as e:
            print(e)

    async def add_db_trip(self, year, trip):
        app = App.get_running_app()
        # POST Request (Add a Pallet)
        data = {
            'year': app.year,
            'trip': app.trip
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}trips", json=data)
                if response:
                    print("add_trip POST response:", response.json())
        except httpx.ConnectError:
            print("Failed to connect to the server.")
