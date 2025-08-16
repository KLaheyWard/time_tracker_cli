import os
from ui_logic.app import App


app = App(os.path.dirname(os.path.abspath(__file__)))
app.start()
    