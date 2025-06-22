import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class VisualizationTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="数据可视化")
        self.create_ui()
    
    def create_ui(self):
        """创建数据可视化界面"""
        # 主容器
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 控制面板
        control_frame = ttk.LabelFrame(main_container, text="绘图控制")
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        control_content = ttk.Frame(control_frame)
        control_content.pack(fill=tk.X, padx=15, pady=15)
        
        # 数据输入 - 第一行
        ttk.Label(control_content, text="X数据:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.plot_x_entry = ttk.Entry(control_content, width=25, style='Modern.TEntry')
        self.plot_x_entry.grid(row=0, column=1, padx=(0, 15), pady=8)
        
        ttk.Label(control_content, text="Y数据:", style='Modern.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=8)
        self.plot_y_entry = ttk.Entry(control_content, width=25, style='Modern.TEntry')
        self.plot_y_entry.grid(row=0, column=3, padx=0, pady=8)
        
        # 函数绘图 - 第二行
        ttk.Label(control_content, text="函数:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.plot_func_entry = ttk.Entry(control_content, width=25, style='Modern.TEntry')
        self.plot_func_entry.grid(row=1, column=1, padx=(0, 15), pady=8)
        
        ttk.Label(control_content, text="范围:", style='Modern.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=8)
        self.plot_range_entry = ttk.Entry(control_content, width=15, style='Modern.TEntry')
        self.plot_range_entry.grid(row=1, column=3, padx=0, pady=8)
        self.plot_range_entry.insert(0, "-10,10")
        
        # 绘图按钮 - 第三行
        button_frame4 = ttk.Frame(control_content)
        button_frame4.grid(row=2, column=0, columnspan=4, pady=(15, 0))
        
        ttk.Button(button_frame4, text="折线图", command=self.plot_line, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame4, text="散点图", command=self.plot_scatter, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame4, text="函数图像", command=self.plot_function, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame4, text="直方图", command=self.plot_histogram, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame4, text="曲线拟合", command=self.plot_curve_fit, style='Modern.TButton').pack(side=tk.LEFT)
        
        # 图形显示区域
        plot_frame = ttk.LabelFrame(main_container, text="图形显示")
        plot_frame.pack(fill=tk.BOTH, expand=True)
        
        plot_content = ttk.Frame(plot_frame)
        plot_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.plot_widget = self.main_window.visualizer.create_figure(plot_content)
        self.plot_widget.pack(fill=tk.BOTH, expand=True)
    
    def plot_line(self):
        """绘制折线图"""
        try:
            x_str = self.plot_x_entry.get()
            y_str = self.plot_y_entry.get()
            
            if not x_str or not y_str:
                messagebox.showwarning("输入错误", "请输入X和Y数据")
                return
                
            x_data = [float(x.strip()) for x in x_str.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            self.main_window.visualizer.plot_line(x_data, y_data)
            
            # 保存绘图数据到current_data
            result_data = {
                'X数据': x_data,
                'Y数据': y_data,
                '图表类型': ['折线图'] * len(x_data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_scatter(self):
        """绘制散点图"""
        try:
            x_str = self.plot_x_entry.get()
            y_str = self.plot_y_entry.get()
            
            if not x_str or not y_str:
                messagebox.showwarning("输入错误", "请输入X和Y数据")
                return
                
            x_data = [float(x.strip()) for x in x_str.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            self.main_window.visualizer.plot_scatter(x_data, y_data)
            
            # 保存绘图数据到current_data
            result_data = {
                'X数据': x_data,
                'Y数据': y_data,
                '图表类型': ['散点图'] * len(x_data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_function(self):
        """绘制函数图像"""
        try:
            func_str = self.plot_func_entry.get()
            range_str = self.plot_range_entry.get()
            
            if not func_str:
                messagebox.showwarning("输入错误", "请输入函数")
                return
                
            # 解析范围
            range_parts = range_str.split(',')
            x_min = float(range_parts[0].strip())
            x_max = float(range_parts[1].strip())
            
            self.main_window.visualizer.plot_function(func_str, x_min, x_max)
            
            # 保存绘图数据到current_data
            result_data = {
                '函数': [func_str],
                '范围': [range_str],
                '图表类型': ['函数图像']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_histogram(self):
        """绘制直方图"""
        try:
            y_str = self.plot_y_entry.get()
            
            if not y_str:
                messagebox.showwarning("输入错误", "请输入Y数据")
                return
                
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            self.main_window.visualizer.plot_histogram(y_data)
            
            # 保存绘图数据到current_data
            result_data = {
                'Y数据': y_data,
                '图表类型': ['直方图'] * len(y_data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_curve_fit(self):
        """绘制曲线拟合"""
        try:
            x_str = self.plot_x_entry.get()
            y_str = self.plot_y_entry.get()
            
            if not x_str or not y_str:
                messagebox.showwarning("输入错误", "请输入X和Y数据")
                return
                
            x_data = [float(x.strip()) for x in x_str.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            self.main_window.visualizer.plot_curve_fit(x_data, y_data)
            
            # 保存绘图数据到current_data
            result_data = {
                'X数据': x_data,
                'Y数据': y_data,
                '图表类型': ['曲线拟合'] * len(x_data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")