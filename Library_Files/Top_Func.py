try:
    from LogViewer_frm import LogViewer
    from Setting_frm import Setting_frm
except:
    from Library_Files.LogViewer_frm import LogViewer
    try:
        from Library_Files.Setting_frm import Setting
    except: pass
from tkinter import *

class Func:
    def __init__(self) -> None:
        pass

    def LogViewer_frm(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = LogViewer(self.new_win)
