#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI主界面
功能：提供图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

# 修正导入路径 - modules 在项目根目录下
from modules.symbolic_calc import SymbolicCalculator
from modules.numerical_calc import NumericalCalculator
from modules.data_processing import DataProcessor
from modules.visualization import DataVisualizer
# excel_handler 在 utils 文件夹中
from utils.excel_handler import ExcelHandler

# 导入各个功能模块的UI和处理器
from .ui_components.symbolic_tab import SymbolicTab
from .ui_components.numerical_tab import NumericalTab
from .ui_components.data_processing_tab import DataProcessingTab
from .ui_components.visualization_tab import VisualizationTab
from .ui_components.excel_tab import ExcelTab

class ScientificCalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("科学计算器")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # 设置现代简约样式
        self.setup_modern_style()
        
        # 初始化计算模块
        self.symbolic_calc = SymbolicCalculator()
        self.numerical_calc = NumericalCalculator()
        self.data_processor = DataProcessor()
        self.visualizer = DataVisualizer()
        self.excel_handler = ExcelHandler()
        
        # 当前数据
        self.current_data = None
        
        # 设置UI
        self.setup_ui()
    
    def setup_modern_style(self):
        """设置现代简约样式"""
        style = ttk.Style()
        
        # 配置主题
        style.theme_use('clam')
        
        # 配置Notebook样式
        style.configure('TNotebook', 
                       background='#f8f9fa',
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
                       background='#e9ecef',
                       foreground='#495057',
                       padding=[20, 10],
                       font=('Microsoft YaHei UI', 10),
                       borderwidth=0)
        
        style.map('TNotebook.Tab',
                 background=[('selected', '#ffffff'),
                           ('active', '#dee2e6')],
                 foreground=[('selected', '#212529')])
        
        # 配置Frame样式
        style.configure('TFrame',
                       background='#ffffff',
                       borderwidth=0)
        
        # 配置LabelFrame样式
        style.configure('TLabelframe',
                       background='#ffffff',
                       borderwidth=1,
                       relief='solid',
                       bordercolor='#dee2e6')
        
        style.configure('TLabelframe.Label',
                       background='#ffffff',
                       foreground='#495057',
                       font=('Microsoft YaHei UI', 10, 'bold'))
        
        # 配置Button样式
        style.configure('Modern.TButton',
                       background='#007bff',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=[15, 8],
                       font=('Microsoft YaHei UI', 9))
        
        style.map('Modern.TButton',
                 background=[('active', '#0056b3'),
                           ('pressed', '#004085')])
        
        # 配置Entry样式
        style.configure('Modern.TEntry',
                       fieldbackground='#ffffff',
                       borderwidth=1,
                       relief='solid',
                       bordercolor='#ced4da',
                       padding=[10, 8],
                       font=('Microsoft YaHei UI', 9))
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', '#007bff')])
        
        # 配置Combobox样式
        style.configure('Modern.TCombobox',
                       fieldbackground='#ffffff',
                       borderwidth=1,
                       relief='solid',
                       bordercolor='#ced4da',
                       padding=[10, 8],
                       font=('Microsoft YaHei UI', 9))
        
        # 配置Label样式
        style.configure('Modern.TLabel',
                       background='#ffffff',
                       foreground='#495057',
                       font=('Microsoft YaHei UI', 9))
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主容器
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建标题
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, 
                               text="科学计算工具",
                               font=('Microsoft YaHei UI', 18, 'bold'),
                               foreground='#212529',
                               background='#f8f9fa')
        title_label.pack()
        
        # 创建主选项卡
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个选项卡
        self.symbolic_tab = SymbolicTab(self.notebook, self)
        self.numerical_tab = NumericalTab(self.notebook, self)
        self.data_processing_tab = DataProcessingTab(self.notebook, self)
        self.visualization_tab = VisualizationTab(self.notebook, self)
        self.excel_tab = ExcelTab(self.notebook, self)
    
    def save_excel_data(self):
        """保存Excel数据"""
        if self.current_data is not None:
            file_path = filedialog.asksaveasfilename(
                title="保存Excel文件",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if file_path:
                result = self.excel_handler.save_excel(self.current_data, file_path)
                if result == "保存成功":
                    messagebox.showinfo("成功", f"数据已保存到: {file_path}")
                else:
                    messagebox.showerror("错误", result)
        else:
            messagebox.showwarning("警告", "没有数据可保存")
    
    def run(self):
        """运行GUI应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ScientificCalculatorGUI()
    app.run()

