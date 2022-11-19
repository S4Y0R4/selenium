from gui_setup import AutoPosterGUI
from poster import Poster

poster = Poster()
gui = AutoPosterGUI(poster)
poster.bind_gui(gui)
poster.start_driver()
# win.event_generate("posting_started")
