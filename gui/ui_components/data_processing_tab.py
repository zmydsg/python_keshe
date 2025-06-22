import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class DataProcessingTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="数据处理")
        self.create_ui()
    
    def create_ui(self):
        """创建数据处理界面"""
        # 数据输入框架
        input_frame = ttk.LabelFrame(self.frame, text="数据输入")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="数据:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.data_entry = ttk.Entry(input_frame, width=50)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)
        
        button_frame1 = ttk.Frame(input_frame)
        button_frame1.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(button_frame1, text="统计分析", command=self.data_statistics).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame1, text="异常值检测", command=self.data_outliers).pack(side=tk.LEFT, padx=2)
        
        # 曲线拟合框架
        fit_frame = ttk.LabelFrame(self.frame, text="曲线拟合")
        fit_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(fit_frame, text="X数据:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.x_data_entry = ttk.Entry(fit_frame, width=25)
        self.x_data_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(fit_frame, text="Y数据:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.y_data_entry = ttk.Entry(fit_frame, width=25)
        self.y_data_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(fit_frame, text="拟合类型:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.fit_type_combo = ttk.Combobox(fit_frame, values=["linear", "polynomial", "exponential"], width=15)
        self.fit_type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.fit_type_combo.set("linear")
        
        ttk.Button(fit_frame, text="曲线拟合", command=self.curve_fitting).grid(row=1, column=2, padx=5, pady=5)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(self.frame, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.data_result_text = tk.Text(result_frame, height=15)
        data_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.data_result_text.yview)
        self.data_result_text.configure(yscrollcommand=data_scrollbar.set)
        self.data_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        data_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def data_statistics(self):
        """执行数据统计分析"""
        try:
            data_str = self.data_entry.get()
            if not data_str:
                messagebox.showwarning("输入错误", "请输入数据")
                return
                
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            result = self.main_window.data_processor.basic_statistics(data)
            
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"数据: {data_str}\n")
            self.data_result_text.insert(tk.END, f"统计结果:\n")
            for key, value in result.items():
                self.data_result_text.insert(tk.END, f"{key}: {value}\n")
            
            # 保存结果到current_data
            result_data = {
                '原始数据': [data_str],
                '数据点数': [result['数据点数']],
                '平均值': [result['平均值']],
                '中位数': [result['中位数']],
                '标准差': [result['标准差']],
                '方差': [result['方差']],
                '最小值': [result['最小值']],
                '最大值': [result['最大值']],
                '操作类型': ['数据统计']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def data_outliers(self):
        """执行异常值检测"""
        try:
            data_str = self.data_entry.get()
            if not data_str:
                messagebox.showwarning("输入错误", "请输入数据")
                return
                
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            result = self.main_window.data_processor.outlier_detection(data, method='iqr')
            
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"数据: {data_str}\n")
            self.data_result_text.insert(tk.END, f"异常值检测结果:\n")
            self.data_result_text.insert(tk.END, f"异常值索引: {result['异常值索引']}\n")
            self.data_result_text.insert(tk.END, f"异常值: {result['异常值']}\n")
            self.data_result_text.insert(tk.END, f"正常值: {result['正常值']}\n")
            
            # 保存结果到current_data
            max_len = max(len(result['异常值']), len(result['正常值']))
            result_data = {
                '原始数据': [data_str] * max_len,
                '异常值': result['异常值'] + [None] * (max_len - len(result['异常值'])),
                '正常值': result['正常值'] + [None] * (max_len - len(result['正常值'])),
                '操作类型': ['异常值检测'] * max_len
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def curve_fitting(self):
        """执行曲线拟合"""
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
            
            # 获取拟合结果
            result = self.main_window.data_processor.curve_fitting(x_data, y_data, fit_type)
            
            # 显示文本结果
            self.data_result_text.delete(1.0, tk.END)
            if isinstance(result, dict):
                self.data_result_text.insert(tk.END, f"曲线拟合结果 ({fit_type}):\n")
                self.data_result_text.insert(tk.END, f"拟合方程: {result['拟合方程']}\n")
                self.data_result_text.insert(tk.END, f"R²: {result['R²']:.4f}\n")
                
                # 保存结果到current_data
                result_data = {
                    'X原始数据': x_data,
                    'Y原始数据': y_data,
                    'Y拟合数据': result['拟合数据'],
                    '拟合方程': [result['拟合方程']] * len(x_data),
                    'R²值': [result['R²']] * len(x_data),
                    '拟合类型': [fit_type] * len(x_data)
                }
                self.main_window.current_data = pd.DataFrame(result_data)
                
            else:
                self.data_result_text.insert(tk.END, f"错误: {result}")
                return
            
            # 绘制拟合图像
            plot_result = self.main_window.visualizer.plot_curve_fitting(x_data, y_data, fit_type)
            self.data_result_text.insert(tk.END, f"\n图像: {plot_result}")
            
        except Exception as e:
            self.data_result_text.delete(1.0, tk.END)
            self.data_result_text.insert(tk.END, f"错误: {str(e)}")