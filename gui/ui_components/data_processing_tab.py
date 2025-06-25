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
        # 主容器
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 数据输入框架
        input_frame = ttk.LabelFrame(main_container, text="数据输入")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 内容容器
        input_content = ttk.Frame(input_frame)
        input_content.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(input_content, text="数据:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.data_entry = ttk.Entry(input_content, width=50, style='Modern.TEntry')
        self.data_entry.grid(row=0, column=1, padx=(0, 15), pady=8, sticky=tk.EW)
        
        button_frame1 = ttk.Frame(input_content)
        button_frame1.grid(row=0, column=2, padx=0, pady=8)
        
        ttk.Button(button_frame1, text="统计分析", command=self.data_statistics, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame1, text="异常值检测", command=self.data_outliers, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame1, text="保存到Excel", command=self.save_to_excel, style='Modern.TButton').pack(side=tk.LEFT)
        
        # 配置列权重
        input_content.columnconfigure(1, weight=1)
        
        # 曲线拟合框架
        fit_frame = ttk.LabelFrame(main_container, text="曲线拟合")
        fit_frame.pack(fill=tk.X, pady=(0, 15))
        
        fit_content = ttk.Frame(fit_frame)
        fit_content.pack(fill=tk.X, padx=15, pady=15)
        
        # 第一行
        ttk.Label(fit_content, text="X数据:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.x_data_entry = ttk.Entry(fit_content, width=25, style='Modern.TEntry')
        self.x_data_entry.grid(row=0, column=1, padx=(0, 15), pady=8)
        
        ttk.Label(fit_content, text="Y数据:", style='Modern.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=8)
        self.y_data_entry = ttk.Entry(fit_content, width=25, style='Modern.TEntry')
        self.y_data_entry.grid(row=0, column=3, padx=0, pady=8)
        
        # 第二行
        ttk.Label(fit_content, text="拟合类型:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.fit_type_combo = ttk.Combobox(fit_content, values=["linear", "polynomial", "exponential"], width=22, style='Modern.TCombobox')
        self.fit_type_combo.grid(row=1, column=1, padx=(0, 15), pady=8)
        self.fit_type_combo.set("linear")
        
        ttk.Button(fit_content, text="曲线拟合", command=self.curve_fitting, style='Modern.TButton').grid(row=1, column=2, padx=0, pady=8, sticky=tk.W)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(main_container, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_content = ttk.Frame(result_frame)
        result_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.data_result_text = tk.Text(result_content, 
                                       height=15,
                                       font=('Consolas', 10),
                                       bg='#f8f9fa',
                                       fg='#495057',
                                       borderwidth=1,
                                       relief='solid',
                                       selectbackground='#007bff',
                                       selectforeground='white')
        data_scrollbar = ttk.Scrollbar(result_content, orient=tk.VERTICAL, command=self.data_result_text.yview)
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
            
            # 修复：使用正确的键名
            result_data = {
                '原始数据': [data_str],
                '数据点数': [result['数据点数']],  # 修复：使用正确的键名
                '平均值': [result['平均值']],      # 修复：从'均值'改为'平均值'
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
    
    def save_to_excel(self):
        """保存数据处理结果到Excel"""
        if self.main_window.current_data is not None:
            self.main_window.save_excel_data()
        else:
            messagebox.showwarning("警告", "没有数据可保存，请先执行数据处理操作")