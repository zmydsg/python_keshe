#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化模块
功能：绘制折线图、曲线图、散点图等
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class DataVisualizer:
    def __init__(self):
        self.figure = None
        self.canvas = None
    
    def create_figure(self, parent_widget):
        """创建matplotlib图形"""
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, parent_widget)
        return self.canvas.get_tk_widget()
    
    def plot_line(self, x_data, y_data, title="折线图", xlabel="X轴", ylabel="Y轴", label="数据"):
        """绘制折线图"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_data, y_data, marker='o', label=label)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return "折线图绘制成功"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def plot_scatter(self, x_data, y_data, title="散点图", xlabel="X轴", ylabel="Y轴", label="数据"):
        """绘制散点图"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.scatter(x_data, y_data, alpha=0.7, label=label)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return "散点图绘制成功"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def plot_function(self, func_str, x_range=(-10, 10), num_points=1000, title="函数图像"):
        """绘制函数图像"""
        try:
            x = np.linspace(x_range[0], x_range[1], num_points)
            
            # 安全计算函数值
            import math
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                'x': x, 'np': np
            })
            
            y = eval(func_str, {"__builtins__": {}}, allowed_names)
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, label=f'y = {func_str}')
            ax.set_title(title)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return "函数图像绘制成功"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def plot_histogram(self, data, bins=30, title="直方图", xlabel="值", ylabel="频数"):
        """绘制直方图"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.hist(data, bins=bins, alpha=0.7, edgecolor='black')
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return "直方图绘制成功"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def plot_multiple_lines(self, data_sets, title="多线图", xlabel="X轴", ylabel="Y轴"):
        """绘制多条线"""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            for i, (x_data, y_data, label) in enumerate(data_sets):
                ax.plot(x_data, y_data, marker='o', label=label)
            
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.canvas.draw()
            return "多线图绘制成功"
        except Exception as e:
            return f"错误: {str(e)}"