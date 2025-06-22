from tkinter import *
from tkinter import ttk

class BaseTab:
    """选项卡基类"""
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        self.setup_tab()
        
    def setup_tab(self):
        """设置选项卡，子类需要重写此方法"""
        raise NotImplementedError("子类必须实现setup_tab方法")