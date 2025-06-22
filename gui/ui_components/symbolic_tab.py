import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class SymbolicTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="符号计算")
        self.create_ui()
    
    def create_ui(self):
        """创建符号计算界面"""
        # 输入框架
        input_frame = ttk.LabelFrame(self.frame, text="输入")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="表达式:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.symbolic_expr_entry = ttk.Entry(input_frame, width=40)
        self.symbolic_expr_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="变量:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.symbolic_var_entry = ttk.Entry(input_frame, width=10)
        self.symbolic_var_entry.grid(row=0, column=3, padx=5, pady=5)
        self.symbolic_var_entry.insert(0, "x")
        
        # 操作按钮框架
        button_frame = ttk.LabelFrame(self.frame, text="操作")
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="求导", command=self.symbolic_differentiate).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="积分", command=self.symbolic_integrate).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="求解方程", command=self.symbolic_solve).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="傅里叶变换", command=self.symbolic_fourier).grid(row=0, column=3, padx=5, pady=5)
        
        # 结果显示框架
        result_frame = ttk.LabelFrame(self.frame, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.symbolic_result_text = tk.Text(result_frame, height=15)
        symbolic_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.symbolic_result_text.yview)
        self.symbolic_result_text.configure(yscrollcommand=symbolic_scrollbar.set)
        self.symbolic_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        symbolic_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def symbolic_differentiate(self):
        """执行符号求导"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result_str, result_expr = self.main_window.symbolic_calc.differentiate(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"求导结果: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '原表达式': [expression],
                '变量': [variable],
                '求导结果': [result_str],
                '操作类型': ['符号求导']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def symbolic_integrate(self):
        """执行符号积分"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result_str, result_expr = self.main_window.symbolic_calc.integrate_symbolic(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"积分结果: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '原表达式': [expression],
                '变量': [variable],
                '积分结果': [result_str],
                '操作类型': ['符号积分']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def symbolic_solve(self):
        """执行符号方程求解"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入方程")
                return
                
            result_str, solutions = self.main_window.symbolic_calc.solve_equation(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"方程: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"求解结果: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '原方程': [expression],
                '变量': [variable],
                '求解结果': [result_str],
                '操作类型': ['符号求解']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def symbolic_fourier(self):
        """执行傅里叶变换计算"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 't'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            result_str, _ = self.main_window.symbolic_calc.fourier_transform_calc(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"傅里叶变换结果: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '原表达式': [expression],
                '变量': [variable],
                '傅里叶变换结果': [result_str],
                '操作类型': ['傅里叶变换']
            }
            self.main_window.current_data = pd.DataFrame(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")