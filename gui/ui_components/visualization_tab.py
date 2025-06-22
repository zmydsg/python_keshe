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
        # 控制面板
        control_frame = ttk.LabelFrame(self.frame, text="绘图控制")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 数据输入
        ttk.Label(control_frame, text="X数据:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.plot_x_entry = ttk.Entry(control_frame, width=25)
        self.plot_x_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Y数据:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.plot_y_entry = ttk.Entry(control_frame, width=25)
        self.plot_y_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # 函数绘图
        ttk.Label(control_frame, text="函数:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.plot_func_entry = ttk.Entry(control_frame, width=25)
        self.plot_func_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="范围:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.plot_range_entry = ttk.Entry(control_frame, width=15)
        self.plot_range_entry.grid(row=1, column=3, padx=5, pady=5)
        self.plot_range_entry.insert(0, "-10,10")
        
        # 绘图按钮
        button_frame4 = ttk.Frame(control_frame)
        button_frame4.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame4, text="折线图", command=self.plot_line).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame4, text="散点图", command=self.plot_scatter).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame4, text="函数图像", command=self.plot_function).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame4, text="直方图", command=self.plot_histogram).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame4, text="曲线拟合", command=self.plot_curve_fit).pack(side=tk.LEFT, padx=5)
        
        # 图形显示区域
        plot_frame = ttk.LabelFrame(self.frame, text="图形显示")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.plot_widget = self.main_window.visualizer.create_figure(plot_frame)
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
                
            try:
                x_min, x_max = map(float, range_str.split(','))
            except:
                messagebox.showerror("错误", "范围格式错误，请使用 min,max 格式")
                return
            
            self.main_window.visualizer.plot_function(func_str, x_min, x_max)
            
            # 保存函数绘图信息到current_data
            result_data = {
                '函数': [func_str],
                'X范围最小值': [x_min],
                'X范围最大值': [x_max],
                '图表类型': ['函数图像']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_histogram(self):
        """绘制直方图"""
        try:
            data_str = self.plot_x_entry.get()
            
            if not data_str:
                messagebox.showwarning("输入错误", "请输入数据")
                return
                
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            
            self.main_window.visualizer.plot_histogram(data)
            
            # 保存直方图数据到current_data
            result_data = {
                '数据': data,
                '图表类型': ['直方图'] * len(data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")
    
    def plot_curve_fit(self):
        """在可视化标签页中绘制曲线拟合"""
        try:
            x_str = self.plot_x_entry.get()
            y_str = self.plot_y_entry.get()
            
            if not x_str or not y_str:
                messagebox.showwarning("输入错误", "请输入X和Y数据")
                return
                
            x_data = [float(x.strip()) for x in x_str.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            if len(x_data) != len(y_data):
                messagebox.showwarning("输入错误", "X和Y数据长度不一致")
                return
            
            # 默认使用线性拟合
            fit_result = self.main_window.data_processor.curve_fitting(x_data, y_data, 'linear')
            
            if isinstance(fit_result, str):  # 错误情况
                messagebox.showerror("错误", fit_result)
                return
            
            # 绘制拟合图像
            self.main_window.visualizer.plot_curve_fitting(x_data, y_data, 'linear')
            
            # 将拟合结果保存到current_data中
            result_data = {
                'X原始数据': x_data,
                'Y原始数据': y_data,
                'Y拟合数据': fit_result['拟合数据'],
                '拟合方程': [fit_result['拟合方程']] * len(x_data),
                'R²值': [fit_result['R²']] * len(x_data)
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
            messagebox.showinfo("成功", f"曲线拟合完成！\n{fit_result['拟合方程']}\nR² = {fit_result['R²']:.4f}\n\n现在可以点击'保存结果'按钮保存拟合数据。")
            
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")