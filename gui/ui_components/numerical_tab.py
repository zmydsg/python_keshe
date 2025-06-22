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
        # 基本运算框架
        basic_frame = ttk.LabelFrame(self.frame, text="基本运算")
        basic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="表达式:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.numerical_expr_entry = ttk.Entry(basic_frame, width=40)
        self.numerical_expr_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(basic_frame, text="计算", command=self.numerical_calculate).grid(row=0, column=2, padx=5, pady=5)
        
        # 高级运算框架
        advanced_frame = ttk.LabelFrame(self.frame, text="高级运算")
        advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="函数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.numerical_func_entry = ttk.Entry(advanced_frame, width=25)
        self.numerical_func_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(advanced_frame, text="变量:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.numerical_var_entry = ttk.Entry(advanced_frame, width=10)
        self.numerical_var_entry.grid(row=0, column=3, padx=5, pady=5)
        self.numerical_var_entry.insert(0, "x")
        
        ttk.Label(advanced_frame, text="点/范围:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.numerical_point_entry = ttk.Entry(advanced_frame, width=25)
        self.numerical_point_entry.grid(row=1, column=1, padx=5, pady=5)
        
        button_frame2 = ttk.Frame(advanced_frame)
        button_frame2.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        ttk.Button(button_frame2, text="数值求导", command=self.numerical_derivative).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame2, text="数值积分", command=self.numerical_integrate).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame2, text="求解方程", command=self.numerical_solve).pack(side=tk.LEFT, padx=2)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(self.frame, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.numerical_result_text = tk.Text(result_frame, height=15)
        numerical_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.numerical_result_text.yview)
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