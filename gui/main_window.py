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
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
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

