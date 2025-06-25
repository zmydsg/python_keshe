import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class NumericalTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="数值计算")
        self.create_ui()
    
    def create_ui(self):
        """创建数值计算界面"""
        # 主容器
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 基本运算框架
        basic_frame = ttk.LabelFrame(main_container, text="基本运算")
        basic_frame.pack(fill=tk.X, pady=(0, 15))
        
        basic_content = ttk.Frame(basic_frame)
        basic_content.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(basic_content, text="表达式:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.numerical_expr_entry = ttk.Entry(basic_content, width=40, style='Modern.TEntry')
        self.numerical_expr_entry.grid(row=0, column=1, padx=(0, 15), pady=8, sticky=tk.EW)
        
        ttk.Button(basic_content, text="计算", command=self.numerical_calculate, style='Modern.TButton').grid(row=0, column=2, padx=(0, 8), pady=8)
        ttk.Button(basic_content, text="保存到Excel", command=self.save_to_excel, style='Modern.TButton').grid(row=0, column=3, padx=0, pady=8)
        
        basic_content.columnconfigure(1, weight=1)
        
        # 高级运算框架
        advanced_frame = ttk.LabelFrame(main_container, text="高级运算")
        advanced_frame.pack(fill=tk.X, pady=(0, 15))
        
        advanced_content = ttk.Frame(advanced_frame)
        advanced_content.pack(fill=tk.X, padx=15, pady=15)
        
        # 第一行
        ttk.Label(advanced_content, text="函数:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.numerical_func_entry = ttk.Entry(advanced_content, width=25, style='Modern.TEntry')
        self.numerical_func_entry.grid(row=0, column=1, padx=(0, 15), pady=8)
        
        ttk.Label(advanced_content, text="变量:", style='Modern.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=8)
        self.numerical_var_entry = ttk.Entry(advanced_content, width=10, style='Modern.TEntry')
        self.numerical_var_entry.grid(row=0, column=3, padx=0, pady=8)
        self.numerical_var_entry.insert(0, "x")
        
        # 第二行
        ttk.Label(advanced_content, text="点/范围:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.numerical_point_entry = ttk.Entry(advanced_content, width=25, style='Modern.TEntry')
        self.numerical_point_entry.grid(row=1, column=1, padx=(0, 15), pady=8)
        
        button_frame2 = ttk.Frame(advanced_content)
        button_frame2.grid(row=1, column=2, columnspan=2, padx=0, pady=8, sticky=tk.W)
        
        ttk.Button(button_frame2, text="数值求导", command=self.numerical_derivative, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame2, text="数值积分", command=self.numerical_integrate, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame2, text="求解方程", command=self.numerical_solve, style='Modern.TButton').pack(side=tk.LEFT)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(main_container, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_content = ttk.Frame(result_frame)
        result_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.numerical_result_text = tk.Text(result_content, 
                                           height=15,
                                           font=('Consolas', 10),
                                           bg='#f8f9fa',
                                           fg='#495057',
                                           borderwidth=1,
                                           relief='solid',
                                           selectbackground='#007bff',
                                           selectforeground='white')
        numerical_scrollbar = ttk.Scrollbar(result_content, orient=tk.VERTICAL, command=self.numerical_result_text.yview)
        self.numerical_result_text.configure(yscrollcommand=numerical_scrollbar.set)
        self.numerical_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        numerical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def numerical_calculate(self):
        """执行基本数值计算"""
        try:
            expression = self.numerical_expr_entry.get()
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result = self.main_window.numerical_calc.evaluate_expression(expression)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.numerical_result_text.insert(tk.END, f"计算结果: {result}\n")
            
            # 保存结果到current_data
            result_data = {
                '表达式': [expression],
                '计算结果': [result],
                '操作类型': ['数值计算']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def numerical_derivative(self):
        """执行数值求导"""
        try:
            func_str = self.numerical_func_entry.get()
            var = self.numerical_var_entry.get() or 'x'
            point_str = self.numerical_point_entry.get()
            
            if not func_str or not point_str:
                messagebox.showwarning("输入错误", "请输入函数和求导点")
                return
                
            point = float(point_str)
            result = self.main_window.numerical_calc.numerical_derivative(func_str, var, point)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"函数: {func_str}\n")
            self.numerical_result_text.insert(tk.END, f"变量: {var}\n")
            self.numerical_result_text.insert(tk.END, f"求导点: {point}\n")
            self.numerical_result_text.insert(tk.END, f"导数值: {result}\n")
            
            # 保存结果到current_data
            result_data = {
                '函数': [func_str],
                '变量': [var],
                '求导点': [point],
                '导数值': [result],
                '操作类型': ['数值求导']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def numerical_integrate(self):
        """执行数值积分"""
        try:
            func_str = self.numerical_func_entry.get()
            var = self.numerical_var_entry.get() or 'x'
            range_str = self.numerical_point_entry.get()
            
            if not func_str or not range_str:
                messagebox.showwarning("输入错误", "请输入函数和积分范围")
                return
                
            try:
                a, b = map(float, range_str.split(','))
            except:
                messagebox.showerror("错误", "积分范围格式错误，请使用 a,b 格式")
                return
                
            result = self.main_window.numerical_calc.numerical_integration(func_str, var, a, b)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"函数: {func_str}\n")
            self.numerical_result_text.insert(tk.END, f"变量: {var}\n")
            self.numerical_result_text.insert(tk.END, f"积分范围: [{a}, {b}]\n")
            self.numerical_result_text.insert(tk.END, f"积分值: {result}\n")
            
            # 保存结果到current_data
            result_data = {
                '函数': [func_str],
                '变量': [var],
                '积分下限': [a],
                '积分上限': [b],
                '积分值': [result],
                '操作类型': ['数值积分']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def numerical_solve(self):
        """执行数值求解"""
        try:
            func_str = self.numerical_func_entry.get()
            var = self.numerical_var_entry.get() or 'x'
            initial_str = self.numerical_point_entry.get()
            
            if not func_str or not initial_str:
                messagebox.showwarning("输入错误", "请输入函数和初始猜测值")
                return
                
            initial_guess = float(initial_str)
            result = self.main_window.numerical_calc.solve_equation_numerical(func_str, var, initial_guess)
            
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"方程: {func_str} = 0\n")
            self.numerical_result_text.insert(tk.END, f"变量: {var}\n")
            self.numerical_result_text.insert(tk.END, f"初始猜测: {initial_guess}\n")
            self.numerical_result_text.insert(tk.END, f"数值解: {result}\n")
            
            # 保存结果到current_data
            result_data = {
                '方程': [func_str],
                '变量': [var],
                '初始猜测': [initial_guess],
                '数值解': [result],
                '操作类型': ['数值求解']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.numerical_result_text.delete(1.0, tk.END)
            self.numerical_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def save_to_excel(self):
        """保存数值计算结果到Excel"""
        if self.main_window.current_data is not None:
            self.main_window.save_excel_data()
        else:
            messagebox.showwarning("警告", "没有数据可保存，请先执行数值计算操作")