import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class ExcelTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Excel处理")
        self.create_ui()
    
    def create_ui(self):
        """创建Excel处理界面"""
        # 文件操作框架
        file_frame = ttk.LabelFrame(self.frame, text="文件操作")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(file_frame, text="选择Excel文件", command=self.select_excel_file).grid(row=0, column=0, padx=5, pady=5)
        self.excel_file_label = ttk.Label(file_frame, text="未选择文件")
        self.excel_file_label.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(file_frame, text="读取数据", command=self.read_excel_data).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(file_frame, text="保存结果", command=self.main_window.save_excel_data).grid(row=0, column=3, padx=5, pady=5)
        
        # 数据操作框架
        operation_frame = ttk.LabelFrame(self.frame, text="数据操作")
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
        calc_frame = ttk.LabelFrame(self.frame, text="Excel数据计算")
        calc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(calc_frame, text="统计分析", command=self.excel_statistics).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(calc_frame, text="相关性分析", command=self.excel_correlation).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(calc_frame, text="曲线拟合", command=self.excel_curve_fitting).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(calc_frame, text="异常值检测", command=self.excel_outlier_detection).grid(row=0, column=3, padx=5, pady=5)
        
        # 数据显示框架
        data_frame = ttk.LabelFrame(self.frame, text="数据预览")
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
        result_frame = ttk.LabelFrame(self.frame, text="计算结果")
        result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.excel_result_text = tk.Text(result_frame, height=8)
        excel_result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.excel_result_text.yview)
        self.excel_result_text.configure(yscrollcommand=excel_result_scrollbar.set)
        self.excel_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        excel_result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def select_excel_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.main_window.excel_file_path = file_path
            self.excel_file_label.config(text=f"已选择: {file_path.split('/')[-1]}")
    
    def read_excel_data(self):
        """读取Excel数据并更新列选择器"""
        if hasattr(self.main_window, 'excel_file_path'):
            df = self.main_window.excel_handler.read_excel(self.main_window.excel_file_path)
            if isinstance(df, str):  # 错误信息
                messagebox.showerror("错误", df)
            else:
                self.main_window.current_data = df
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
    
    def display_excel_data(self, df):
        """在表格中显示Excel数据"""
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
        
        # 插入数据
        for index, row in df.iterrows():
            self.excel_tree.insert('', 'end', values=list(row))
    
    def import_to_numerical(self):
        """将Excel数据导入到数值计算模块"""
        if self.main_window.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.main_window.current_data.columns:
                data = self.main_window.excel_handler.export_column_to_list(self.main_window.current_data, column)
                if data:
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到数值计算模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_to_data_processing(self):
        """将Excel数据导入到数据处理模块"""
        if self.main_window.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.main_window.current_data.columns:
                data = self.main_window.excel_handler.export_column_to_list(self.main_window.current_data, column)
                if data:
                    # 将数据转换为逗号分隔的字符串并填入数据处理模块
                    data_str = ','.join(map(str, data))
                    self.main_window.data_processing_tab.data_entry.delete(0, tk.END)
                    self.main_window.data_processing_tab.data_entry.insert(0, data_str)
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到数据处理模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_to_visualization(self):
        """将Excel数据导入到可视化模块"""
        if self.main_window.current_data is not None:
            column = self.column_combo.get()
            if column and column in self.main_window.current_data.columns:
                data = self.main_window.excel_handler.export_column_to_list(self.main_window.current_data, column)
                if data:
                    # 将数据转换为逗号分隔的字符串并填入可视化模块
                    data_str = ','.join(map(str, data))
                    self.main_window.visualization_tab.plot_x_entry.delete(0, tk.END)
                    self.main_window.visualization_tab.plot_x_entry.insert(0, data_str)
                    messagebox.showinfo("成功", f"已导入 {len(data)} 个数据点到可视化模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def import_xy_data(self):
        """导入XY数据到相关模块"""
        if self.main_window.current_data is not None:
            x_column = self.x_column_combo.get()
            y_column = self.y_column_combo.get()
            
            if x_column and y_column and x_column in self.main_window.current_data.columns and y_column in self.main_window.current_data.columns:
                x_data = self.main_window.excel_handler.export_column_to_list(self.main_window.current_data, x_column)
                y_data = self.main_window.excel_handler.export_column_to_list(self.main_window.current_data, y_column)
                
                if x_data and y_data:
                    # 将数据转换为逗号分隔的字符串并填入可视化模块
                    x_data_str = ','.join(map(str, x_data))
                    y_data_str = ','.join(map(str, y_data))
                    
                    self.main_window.visualization_tab.plot_x_entry.delete(0, tk.END)
                    self.main_window.visualization_tab.plot_x_entry.insert(0, x_data_str)
                    self.main_window.visualization_tab.plot_y_entry.delete(0, tk.END)
                    self.main_window.visualization_tab.plot_y_entry.insert(0, y_data_str)
                    
                    # 同时填入数据处理模块的曲线拟合
                    self.main_window.data_processing_tab.x_data_entry.delete(0, tk.END)
                    self.main_window.data_processing_tab.x_data_entry.insert(0, x_data_str)
                    self.main_window.data_processing_tab.y_data_entry.delete(0, tk.END)
                    self.main_window.data_processing_tab.y_data_entry.insert(0, y_data_str)
                    
                    messagebox.showinfo("成功", f"已导入 {len(x_data)} 个XY数据点到可视化和数据处理模块")
                else:
                    messagebox.showwarning("警告", "选择的列没有有效数据")
            else:
                messagebox.showwarning("警告", "请选择有效的X和Y列")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def display_excel_result(self, result_text):
        """显示Excel计算结果"""
        self.excel_result_text.delete(1.0, tk.END)
        self.excel_result_text.insert(tk.END, result_text)
    
    def excel_statistics(self):
        """Excel数据统计分析"""
        if self.main_window.current_data is not None:
            try:
                # 选择数值列进行统计
                numeric_columns = self.main_window.current_data.select_dtypes(include=[float, int]).columns
                if len(numeric_columns) == 0:
                    messagebox.showwarning("警告", "没有找到数值列")
                    return
                
                result = self.main_window.data_processor.basic_statistics(self.main_window.current_data[numeric_columns[0]].tolist())
                
                # 构建结果DataFrame
                stats_data = {
                    '统计项': ['均值', '中位数', '标准差', '方差', '最小值', '最大值', '四分位数Q1', '四分位数Q3'],
                    '数值': [result['均值'], result['中位数'], result['标准差'], result['方差'], 
                            result['最小值'], result['最大值'], result['四分位数'][0], result['四分位数'][1]]
                }
                self.main_window.current_data = pd.DataFrame(stats_data)
                
                # 显示结果
                result_text = f"统计分析结果 (列: {numeric_columns[0]}):\n"
                for key, value in result.items():
                    if key == '四分位数':
                        result_text += f"{key}: Q1={value[0]:.4f}, Q3={value[1]:.4f}\n"
                    else:
                        result_text += f"{key}: {value:.4f}\n"
                
                self.display_excel_result(result_text)
                
            except Exception as e:
                messagebox.showerror("错误", f"统计分析失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_correlation(self):
        """Excel数据相关性分析"""
        if self.main_window.current_data is not None:
            try:
                # 选择数值列进行相关性分析
                numeric_columns = self.main_window.current_data.select_dtypes(include=[float, int]).columns
                if len(numeric_columns) < 2:
                    messagebox.showwarning("警告", "至少需要两个数值列进行相关性分析")
                    return
                
                # 计算相关性矩阵
                correlation_matrix = self.main_window.current_data[numeric_columns].corr()
                
                # 保存相关性矩阵到current_data
                self.main_window.current_data = correlation_matrix
                
                # 显示结果
                result_text = "相关性分析结果:\n"
                result_text += correlation_matrix.to_string()
                
                self.display_excel_result(result_text)
                
            except Exception as e:
                messagebox.showerror("错误", f"相关性分析失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_curve_fitting(self):
        """Excel数据曲线拟合"""
        if self.main_window.current_data is not None:
            try:
                # 获取选择的X和Y列
                x_column = self.x_column_combo.get()
                y_column = self.y_column_combo.get()
                
                if not x_column or not y_column:
                    messagebox.showwarning("警告", "请选择X和Y列")
                    return
                
                if x_column not in self.main_window.current_data.columns or y_column not in self.main_window.current_data.columns:
                    messagebox.showwarning("警告", "选择的列不存在")
                    return
                
                x_data = self.main_window.current_data[x_column].dropna().tolist()
                y_data = self.main_window.current_data[y_column].dropna().tolist()
                
                if len(x_data) != len(y_data) or len(x_data) < 2:
                    messagebox.showwarning("警告", "数据长度不一致或数据点太少")
                    return
                
                # 进行线性拟合
                result = self.main_window.data_processor.curve_fitting(x_data, y_data, 'linear')
                
                if isinstance(result, dict):
                    # 构建拟合结果DataFrame
                    fit_data = {
                        'X原始数据': x_data,
                        'Y原始数据': y_data,
                        'Y拟合数据': result['拟合数据'],
                        '拟合方程': [result['拟合方程']] * len(x_data),
                        'R²值': [result['R²']] * len(x_data)
                    }
                    self.main_window.current_data = pd.DataFrame(fit_data)
                    
                    # 显示结果
                    result_text = f"曲线拟合结果:\n"
                    result_text += f"拟合方程: {result['拟合方程']}\n"
                    result_text += f"R²: {result['R²']:.4f}\n"
                    
                    self.display_excel_result(result_text)
                else:
                    messagebox.showerror("错误", f"曲线拟合失败: {result}")
                
            except Exception as e:
                messagebox.showerror("错误", f"曲线拟合失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")
    
    def excel_outlier_detection(self):
        """Excel数据异常值检测"""
        if self.main_window.current_data is not None:
            try:
                # 选择数值列进行异常值检测
                numeric_columns = self.main_window.current_data.select_dtypes(include=[float, int]).columns
                if len(numeric_columns) == 0:
                    messagebox.showwarning("警告", "没有找到数值列")
                    return
                
                column = numeric_columns[0]  # 使用第一个数值列
                data = self.main_window.current_data[column].dropna().tolist()
                
                # 使用IQR方法检测异常值
                outliers_iqr = self.main_window.data_processor.outlier_detection(data, method='iqr')
                outliers_zscore = self.main_window.data_processor.outlier_detection(data, method='zscore')
                
                # 构建异常值检测结果DataFrame
                outlier_data = {
                    '原始数据': data,
                    'IQR异常值': [x in outliers_iqr for x in data],
                    'Z-score异常值': [x in outliers_zscore for x in data]
                }
                self.main_window.current_data = pd.DataFrame(outlier_data)
                
                # 显示结果
                result_text = f"异常值检测结果 (列: {column}):\n"
                result_text += f"IQR方法检测到 {len(outliers_iqr)} 个异常值: {outliers_iqr}\n"
                result_text += f"Z-score方法检测到 {len(outliers_zscore)} 个异常值: {outliers_zscore}\n"
                
                self.display_excel_result(result_text)
                
            except Exception as e:
                messagebox.showerror("错误", f"异常值检测失败: {str(e)}")
        else:
            messagebox.showwarning("警告", "请先读取Excel数据")