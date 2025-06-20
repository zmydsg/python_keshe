#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI主界面
功能：提供图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter.simpledialog
from modules.symbolic_calc import SymbolicCalculator
from modules.numerical_calc import NumericalCalculator
from modules.data_processing import DataProcessor
from modules.visualization import DataVisualizer
from utils.excel_handler import ExcelHandler

class ScientificCalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python科学计算工具")
        self.root.geometry("1200x800")
        
        # 初始化计算模块
        self.symbolic_calc = SymbolicCalculator()
        self.numerical_calc = NumericalCalculator()
        self.data_processor = DataProcessor()
        self.visualizer = DataVisualizer()
        self.excel_handler = ExcelHandler()
        
        # 数据存储
        self.current_data = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 符号计算选项卡
        self.create_symbolic_tab(notebook)
        
        # 数值计算选项卡
        self.create_numerical_tab(notebook)
        
        # 数据处理选项卡
        self.create_data_processing_tab(notebook)
        
        # 数据可视化选项卡
        self.create_visualization_tab(notebook)
        
        # Excel处理选项卡
        self.create_excel_tab(notebook)
    
    def create_symbolic_tab(self, parent):
        """创建符号计算选项卡"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="符号计算")
        
        # 输入框架
        input_frame = ttk.LabelFrame(frame, text="输入")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="表达式:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.symbolic_expr_entry = ttk.Entry(input_frame, width=50)
        self.symbolic_expr_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="变量:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.symbolic_var_entry = ttk.Entry(input_frame, width=20)
        self.symbolic_var_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.symbolic_var_entry.insert(0, "x")
        
        # 操作按钮框架
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="求导", command=self.symbolic_differentiate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="积分", command=self.symbolic_integrate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="求解方程", command=self.symbolic_solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="化简", command=self.symbolic_simplify).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="傅里叶变换", command=self.symbolic_fourier).pack(side=tk.LEFT, padx=5)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(frame, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.symbolic_result_text = tk.Text(result_frame, height=15)
        scrollbar1 = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.symbolic_result_text.yview)
        self.symbolic_result_text.configure(yscrollcommand=scrollbar1.set)
        self.symbolic_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_numerical_tab(self, parent):
        """创建数值计算选项卡"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="数值计算")
        
        # 基本运算框架
        calc_frame = ttk.LabelFrame(frame, text="基本运算")
        calc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(calc_frame, text="表达式:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.numerical_expr_entry = ttk.Entry(calc_frame, width=50)
        self.numerical_expr_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(calc_frame, text="计算", command=self.numerical_calculate).grid(row=0, column=2, padx=5, pady=5)
        
        # 高级运算框架
        advanced_frame = ttk.LabelFrame(frame, text="高级运算")
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="函数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.numerical_func_entry = ttk.Entry(advanced_frame, width=30)
        self.numerical_func_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="x值:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.numerical_x_entry = ttk.Entry(advanced_frame, width=10)
        self.numerical_x_entry.grid(row=0, column=3, padx=5, pady=5)
        
        button_frame2 = ttk.Frame(advanced_frame)
        button_frame2.grid(row=1, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame2, text="数值求导", command=self.numerical_derivative).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="数值积分", command=self.numerical_integration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="求解方程", command=self.numerical_solve).pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        result_frame2 = ttk.LabelFrame(frame, text="结果")
        result_frame2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.numerical_result_text = tk.Text(result_frame2, height=10)
        scrollbar2 = ttk.Scrollbar(result_frame2, orient=tk.VERTICAL, command=self.numerical_result_text.yview)
        self.numerical_result_text.configure(yscrollcommand=scrollbar2.set)
        self.numerical_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_data_processing_tab(self, parent):
        """创建数据处理选项卡"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="数据处理")
        
        # 数据输入框架
        input_frame = ttk.LabelFrame(frame, text="数据输入")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="数据 (用逗号分隔):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.data_entry = ttk.Entry(input_frame, width=60)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)
        
        button_frame3 = ttk.Frame(input_frame)
        button_frame3.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame3, text="统计分析", command=self.data_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame3, text="异常值检测", command=self.data_outliers).pack(side=tk.LEFT, padx=5)
        
        # 曲线拟合框架
        fitting_frame = ttk.LabelFrame(frame, text="曲线拟合")
        fitting_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(fitting_frame, text="X数据:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.x_data_entry = ttk.Entry(fitting_frame, width=30)
        self.x_data_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(fitting_frame, text="Y数据:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.y_data_entry = ttk.Entry(fitting_frame, width=30)
        self.y_data_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(fitting_frame, text="拟合类型:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.fit_type_combo = ttk.Combobox(fitting_frame, values=["linear", "polynomial", "exponential"], width=15)
        self.fit_type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.fit_type_combo.set("linear")
        
        ttk.Button(fitting_frame, text="曲线拟合", command=self.curve_fitting).grid(row=1, column=2, padx=5, pady=5)
        
        # 结果显示
        result_frame3 = ttk.LabelFrame(frame, text="结果")
        result_frame3.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.data_result_text = tk.Text(result_frame3, height=10)
        scrollbar3 = ttk.Scrollbar(result_frame3, orient=tk.VERTICAL, command=self.data_result_text.yview)
        self.data_result_text.configure(yscrollcommand=scrollbar3.set)
        self.data_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_visualization_tab(self, parent):
        """创建数据可视化选项卡"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="数据可视化")
        
        # 控制面板
        control_frame = ttk.LabelFrame(frame, text="绘图控制")
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
        
        # 图形显示区域
        plot_frame = ttk.LabelFrame(frame, text="图形显示")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.plot_widget = self.visualizer.create_figure(plot_frame)
        self.plot_widget.pack(fill=tk.BOTH, expand=True)
    
    def create_excel_tab(self, parent):
        """创建Excel处理选项卡"""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Excel处理")
        
        # 文件操作框架
        file_frame = ttk.LabelFrame(frame, text="文件操作")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(file_frame, text="选择Excel文件", command=self.select_excel_file).grid(row=0, column=0, padx=5, pady=5)
        self.excel_file_label = ttk.Label(file_frame, text="未选择文件")
        self.excel_file_label.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(file_frame, text="读取数据", command=self.read_excel_data).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(file_frame, text="保存结果", command=self.save_excel_data).grid(row=0, column=3, padx=5, pady=5)
        
        # 数据操作框架
        operation_frame = ttk.LabelFrame(frame, text="数据操作")
        operation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 列选择
        ttk.Label(operation_frame, text="选择列:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.column_combo = ttk.Combobox(operation_frame, width=15)
        self.column_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # 操作按钮
        ttk.Button(operation_frame, text="导入到数值计算", command=self.import_to_numerical).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(operation_frame, text="导入到数据处理", command=self.import_to_data_processing).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(operation_frame, text="导入到可视化", command=self.import_to_visualization).grid(row=0, column=4, padx=5, pady=5)
        
        # 双列操作
        ttk.Label(operation_frame, text="X列:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.x_column_combo = ttk.Combobox(operation_frame, width=12)
        self.x_column_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(operation_frame, text="Y列:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.y_column_combo = ttk.Combobox(operation_frame, width=12)
        self.y_column_combo.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Button(operation_frame, text="导入XY数据", command=self.import_xy_data).grid(row=1, column=4, padx=5, pady=5)
        
        # 计算功能框架
        calc_frame = ttk.LabelFrame(frame, text="Excel数据计算")
        calc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(calc_frame, text="统计分析", command=self.excel_statistics).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(calc_frame, text="相关性分析", command=self.excel_correlation).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(calc_frame, text="曲线拟合", command=self.excel_curve_fitting).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(calc_frame, text="异常值检测", command=self.excel_outlier_detection).grid(row=0, column=3, padx=5, pady=5)
        
        # 数据显示框架
        data_frame = ttk.LabelFrame(frame, text="数据预览")
        data_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建表格
        self.excel_tree = ttk.Treeview(data_frame)
        excel_scrollbar_y = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.excel_tree.yview)
        excel_scrollbar_x = ttk.Scrollbar(data_frame, orient=tk.HORIZONTAL, command=self.excel_tree.xview)
        self.excel_tree.configure(yscrollcommand=excel_scrollbar_y.set, xscrollcommand=excel_scrollbar_x.set)
        
        self.excel_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        excel_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        excel_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 结果显示
        result_frame = ttk.LabelFrame(frame, text="计算结果")
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.excel_result_text = tk.Text(result_frame, height=8)
        excel_result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.excel_result_text.yview)
        self.excel_result_text.configure(yscrollcommand=excel_result_scrollbar.set)
        self.excel_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        excel_result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Excel数据集成方法
    def read_excel_data(self):
        """读取Excel数据并更新列选择器"""
        if hasattr(self, 'excel_file_path'):
            df = self.excel_handler.read_excel(self.excel_file_path)
            if isinstance(df, str):  # 错误信息
                messagebox.showerror("错误", df)
            else:
                self.current_data = df
                self.display_excel_data(df)
                
                # 更新列选择器
                columns = list(df.columns)
                self.column_combo['values'] = columns
                self.x_column_combo['values'] = columns
                self.y_column_combo['values'] = columns
                
                if columns:
                    self.column_combo.set(columns[0])
                    if len(columns) >= 2:
                        self.x_column_combo.set(columns[0])
                        self.y_column_combo.set(columns[1])
        else:
            messagebox.showwarning("警告", "请先选择Excel文件")
    
    def import_to_numerical(self):
        """将Excel数据导入到数值计算模块"""
        if self.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.current_data.columns:
                data = self.excel_handler.export_column_to_list(self.current_data, column)
                if data:
                    # 将数据转换为逗号分隔的字符串
                    data_str = ','.join(map(str, data))
                    # 这里需要切换到数值计算选项卡并填入数据
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到数值计算模块")
                    # 可以在这里添加自动切换选项卡的代码
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_to_data_processing(self):
        """将Excel数据导入到数据处理模块"""
        if self.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.current_data.columns:
                data = self.excel_handler.export_column_to_list(self.current_data, column)
                if data:
                    # 将数据转换为逗号分隔的字符串并填入数据处理模块
                    data_str = ','.join(map(str, data))
                    self.data_entry.delete(0, tk.END)
                    self.data_entry.insert(0, data_str)
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到数据处理模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_to_visualization(self):
        """将Excel数据导入到可视化模块"""
        if self.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.current_data.columns:
                data = self.excel_handler.export_column_to_list(self.current_data, column)
                if data:
                    # 将数据转换为逗号分隔的字符串并填入可视化模块
                    data_str = ','.join(map(str, data))
                    self.plot_x_entry.delete(0, tk.END)
                    self.plot_x_entry.insert(0, data_str)
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到可视化模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_xy_data(self):
        """导入XY数据到相关模块"""
        if self.current_data is not None:
            x_column = self.x_column_combo.get()
            y_column = self.y_column_combo.get()
            
            if x_column and y_column and x_column in self.current_data.columns and y_column in self.current_data.columns:
                x_data = self.excel_handler.export_column_to_list(self.current_data, x_column)
                y_data = self.excel_handler.export_column_to_list(self.current_data, y_column)
                
                if x_data and y_data:
                    # 确保数据长度一致
                    min_len = min(len(x_data), len(y_data))
                    x_data = x_data[:min_len]
                    y_data = y_data[:min_len]
                    
                    # 导入到数据处理模块
                    x_str = ','.join(map(str, x_data))
                    y_str = ','.join(map(str, y_data))
                    
                    self.x_data_entry.delete(0, tk.END)
                    self.x_data_entry.insert(0, x_str)
                    self.y_data_entry.delete(0, tk.END)
                    self.y_data_entry.insert(0, y_str)
                    
                    # 同时导入到可视化模块
                    self.plot_x_entry.delete(0, tk.END)
                    self.plot_x_entry.insert(0, x_str)
                    self.plot_y_entry.delete(0, tk.END)
                    self.plot_y_entry.insert(0, y_str)
                    
                    messagebox.showinfo("成功", f"已导入 {min_len} 对XY数据点")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的X和Y列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    # Excel数据计算方法
    def excel_statistics(self):
        """对Excel数据进行统计分析"""
        if self.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.current_data.columns:
                data = self.excel_handler.export_column_to_list(self.current_data, column)
                if data:
                    result = self.data_processor.basic_statistics(data)
                    self.display_excel_result(f"列 '{column}' 的统计分析:\n{result}")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_correlation(self):
        """Excel数据相关性分析"""
        if self.current_data is not None:
            x_column = self.x_column_combo.get()
            y_column = self.y_column_combo.get()
            
            if x_column and y_column and x_column in self.current_data.columns and y_column in self.current_data.columns:
                x_data = self.excel_handler.export_column_to_list(self.current_data, x_column)
                y_data = self.excel_handler.export_column_to_list(self.current_data, y_column)
                
                if x_data and y_data:
                    min_len = min(len(x_data), len(y_data))
                    x_data = x_data[:min_len]
                    y_data = y_data[:min_len]
                    
                    result = self.data_processor.correlation_analysis(x_data, y_data)
                    self.display_excel_result(f"'{x_column}' 与 '{y_column}' 的相关性分析:\n{result}")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的X和Y列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_curve_fitting(self):
        """Excel数据曲线拟合"""
        if self.current_data is not None:
            x_column = self.x_column_combo.get()
            y_column = self.y_column_combo.get()
            
            if x_column and y_column and x_column in self.current_data.columns and y_column in self.current_data.columns:
                x_data = self.excel_handler.export_column_to_list(self.current_data, x_column)
                y_data = self.excel_handler.export_column_to_list(self.current_data, y_column)
                
                if x_data and y_data:
                    min_len = min(len(x_data), len(y_data))
                    x_data = x_data[:min_len]
                    y_data = y_data[:min_len]
                    
                    # 进行线性拟合
                    result = self.data_processor.curve_fitting(x_data, y_data, 'linear')
                    self.display_excel_result(f"'{x_column}' 与 '{y_column}' 的曲线拟合:\n{result}")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的X和Y列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_outlier_detection(self):
        """Excel数据异常值检测"""
        if self.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.current_data.columns:
                data = self.excel_handler.export_column_to_list(self.current_data, column)
                if data:
                    result = self.data_processor.outlier_detection(data)
                    self.display_excel_result(f"列 '{column}' 的异常值检测:\n{result}")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def display_excel_result(self, result):
        """显示Excel计算结果"""
        self.excel_result_text.insert(tk.END, str(result) + "\n\n")
        self.excel_result_text.see(tk.END)
        
    def display_excel_data(self, df):
        # 清空现有数据
        for item in self.excel_tree.get_children():
            self.excel_tree.delete(item)
        
        # 设置列
        self.excel_tree['columns'] = list(df.columns)
        self.excel_tree['show'] = 'headings'
        
        # 设置列标题
        for col in df.columns:
            self.excel_tree.heading(col, text=col)
            self.excel_tree.column(col, width=100)
        
        # 插入数据（只显示前100行）
        for index, row in df.head(100).iterrows():
            self.excel_tree.insert('', 'end', values=list(row))
    
    def save_excel_data(self):
        if self.current_data is not None:
            file_path = filedialog.asksaveasfilename(
                title="保存Excel文件",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if file_path:
                result = self.excel_handler.write_excel(self.current_data, file_path)
                messagebox.showinfo("信息", result)
        else:
            messagebox.showwarning("警告", "没有数据可保存")
    
    def symbolic_differentiate(self):
        """符号求导"""  
        expression = self.symbolic_expr_entry.get()
        variable = self.symbolic_var_entry.get()
        
        if not expression:
            messagebox.showwarning("警告", "请输入表达式")
            return
        
        if not variable:
            variable = "x"  # 默认变量
        
        result, _ = self.symbolic_calc.differentiate(expression, variable)
        self.symbolic_result_text.delete(1.0, tk.END)
        self.symbolic_result_text.insert(tk.END, f"表达式 {expression} 关于 {variable} 的导数:\n{result}")

    def symbolic_integrate(self):
        """符号积分"""
        expression = self.symbolic_expr_entry.get()
        variable = self.symbolic_var_entry.get()
        
        if not expression:
            messagebox.showwarning("警告", "请输入表达式")
            return
        
        if not variable:
            variable = "x"  # 默认变量
        
        # 默认进行不定积分
        result, _ = self.symbolic_calc.integrate_symbolic(expression, variable)
        self.symbolic_result_text.delete(1.0, tk.END)
        self.symbolic_result_text.insert(tk.END, f"表达式 {expression} 关于 {variable} 的积分:\n{result}")

    def symbolic_solve(self):
        """求解方程"""
        equation = self.symbolic_expr_entry.get()
        variable = self.symbolic_var_entry.get()
        
        if not equation:
            messagebox.showwarning("警告", "请输入方程")
            return
        
        if not variable:
            variable = "x"  # 默认变量
        
        solutions, _ = self.symbolic_calc.solve_equation(equation, variable)
        
        # 显示结果
        self.symbolic_result_text.delete(1.0, tk.END)
        if solutions:
            self.symbolic_result_text.insert(tk.END, f"方程 {equation} = 0 关于 {variable} 的解：\n")
            for i, sol in enumerate(solutions):
                self.symbolic_result_text.insert(tk.END, f"解 {i+1}: {sol}\n")
        else:
            self.symbolic_result_text.insert(tk.END, f"方程 {equation} = 0 关于 {variable} 没有解")

    def symbolic_simplify(self):
        """化简表达式"""
        expression = self.symbolic_expr_entry.get()
        
        if not expression:
            messagebox.showwarning("警告", "请输入表达式")
            return
        
        result, _ = self.symbolic_calc.simplify_expression(expression)
        
        # 显示结果
        self.symbolic_result_text.delete(1.0, tk.END)
        self.symbolic_result_text.insert(tk.END, f"表达式 {expression} 的化简结果：\n{result}")

    def symbolic_fourier(self):
        """执行傅里叶变换计算"""
        try:
            expression = self.symbolic_expression_entry.get()
            variable = self.symbolic_variable_entry.get() or 't'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result_str, _ = self.symbolic_calculator.fourier_transform_calc(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"傅里叶变换结果: {result_str}\n")
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    def numerical_calculate(self):
        """执行基本数值计算"""
        try:
            expression = self.numerical_expr_entry.get()
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result = self.numerical_calc.basic_arithmetic(expression)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.numerical_result_text.insert(tk.END, f"计算结果: {result}\n")
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")

    # 在ScientificCalculatorGUI类中添加以下缺失的方法：

# 1. 数值计算相关方法
    def numerical_derivative(self):
        """数值求导"""
        try:
            func_str = self.numerical_func_entry.get()
            x_val_str = self.numerical_x_entry.get()
            
            if not func_str:
                messagebox.showwarning("输入错误", "请输入函数")
                return
            if not x_val_str:
                messagebox.showwarning("输入错误", "请输入x值")
                return
                
            x_val = float(x_val_str)
            
            # 创建函数
            def func(x):
                import math
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                allowed_names['x'] = x
                return eval(func_str, {"__builtins__": {}}, allowed_names)
            
            result = self.numerical_calc.calculate_derivative(func, x_val)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"函数: {func_str}\n")
            self.numerical_result_text.insert(tk.END, f"在x={x_val}处的导数: {result}\n")
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")

    def numerical_integration(self):
        """数值积分"""
        try:
            func_str = self.numerical_func_entry.get()
            
            if not func_str:
                messagebox.showwarning("输入错误", "请输入函数")
                return
                
            # 简单的积分范围输入对话框
            range_str = tk.simpledialog.askstring("积分范围", "请输入积分范围 (格式: a,b):")
            if not range_str:
                return
                
            try:
                a, b = map(float, range_str.split(','))
            except:
                messagebox.showerror("错误", "积分范围格式错误，请使用 a,b 格式")
                return
            
            result, error = self.numerical_calc.numerical_integration(func_str, a, b)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"函数: {func_str}\n")
            self.numerical_result_text.insert(tk.END, f"积分区间: [{a}, {b}]\n")
            self.numerical_result_text.insert(tk.END, f"积分结果: {result}\n")
            if error:
                self.numerical_result_text.insert(tk.END, f"误差估计: {error}\n")
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")

    def numerical_solve(self):
        """数值求解方程"""
        try:
            func_str = self.numerical_func_entry.get()
            
            if not func_str:
                messagebox.showwarning("输入错误", "请输入函数")
                return
                
            # 初始猜测值
            guess_str = tk.simpledialog.askstring("初始猜测", "请输入初始猜测值:", initialvalue="0")
            if guess_str is None:
                return
                
            try:
                initial_guess = float(guess_str)
            except:
                messagebox.showerror("错误", "初始猜测值必须是数字")
                return
            
            result = self.numerical_calc.solve_equation_numerical(func_str, initial_guess)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"方程: {func_str} = 0\n")
            self.numerical_result_text.insert(tk.END, f"初始猜测: {initial_guess}\n")
            self.numerical_result_text.insert(tk.END, f"数值解: {result}\n")
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")

    # 2. 数据处理相关方法
    def data_statistics(self):
        """数据统计分析"""
        try:
            data_str = self.data_entry.get()
            if not data_str:
                messagebox.showwarning("输入错误", "请输入数据")
                return
                
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            if not data:
                messagebox.showwarning("输入错误", "没有有效数据")
                return
                
            result = self.data_processor.basic_statistics(data)
            
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"数据统计分析:\n{result}\n")
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")

    def data_outliers(self):
        """异常值检测"""
        try:
            data_str = self.data_entry.get()
            if not data_str:
                messagebox.showwarning("输入错误", "请输入数据")
                return
                
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            if not data:
                messagebox.showwarning("输入错误", "没有有效数据")
                return
                
            result = self.data_processor.outlier_detection(data)
            
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"异常值检测:\n{result}\n")
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")

    def curve_fitting(self):
        """曲线拟合"""
        try:
            x_str = self.x_data_entry.get()
            y_str = self.y_data_entry.get()
            fit_type = self.fit_type_combo.get()
            
            if not x_str or not y_str:
                messagebox.showwarning("输入错误", "请输入X和Y数据")
                return
                
            x_data = [float(x.strip()) for x in x_str.split(',') if x.strip()]
            y_data = [float(y.strip()) for y in y_str.split(',') if y.strip()]
            
            if len(x_data) != len(y_data):
                messagebox.showwarning("输入错误", "X和Y数据长度不一致")
                return
                
            result = self.data_processor.curve_fitting(x_data, y_data, fit_type)
            
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"曲线拟合结果 ({fit_type}):\n{result}\n")
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")

    # 3. 数据可视化相关方法
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
            
            self.visualizer.plot_line(x_data, y_data)
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
            
            self.visualizer.plot_scatter(x_data, y_data)
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
            
            self.visualizer.plot_function(func_str, x_min, x_max)
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
            
            self.visualizer.plot_histogram(data)
        except Exception as e:
            messagebox.showerror("错误", f"绘图错误: {str(e)}")

    # 4. Excel文件处理方法
    def select_excel_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.excel_file_path = file_path
            self.excel_file_label.config(text=f"已选择: {file_path.split('/')[-1]}")

    # 5. 修复symbolic_fourier方法中的错误
    def symbolic_fourier(self):
        """执行傅里叶变换计算"""
        try:
            expression = self.symbolic_expr_entry.get()  # 修复：使用正确的变量名
            variable = self.symbolic_var_entry.get() or 't'  # 修复：使用正确的变量名
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result_str, _ = self.symbolic_calc.fourier_transform_calc(expression, variable)  # 修复：使用正确的对象名
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"傅里叶变换结果: {result_str}\n")
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")


    def run(self):
        """运行GUI应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ScientificCalculatorGUI()
    app.run()

