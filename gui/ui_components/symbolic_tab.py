import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SymbolicTab:
    def __init__(self, parent, main_window):
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="符号计算")
        self.figure = plt.Figure(figsize=(3, 2), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.create_ui()
        self.latex_preview = self.figure.add_subplot(111)
        self.latex_preview.axis('off')

    def create_ui(self):
        """创建符号计算界面"""
        # 主容器
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 输入框架
        input_frame = ttk.LabelFrame(main_container, text="输入")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_content = ttk.Frame(input_frame)
        input_content.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(input_content, text="表达式:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=8)
        self.symbolic_expr_entry = ttk.Entry(input_content, width=40, style='Modern.TEntry')
        self.symbolic_expr_entry.grid(row=0, column=1, padx=(0, 15), pady=8, sticky=tk.EW)
        self.symbolic_expr_entry.bind('<KeyRelease>', self.update_latex_preview)

        ttk.Label(input_content, text="变量:", style='Modern.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=8)
        self.symbolic_var_entry = ttk.Entry(input_content, width=10, style='Modern.TEntry')
        self.symbolic_var_entry.grid(row=0, column=3, padx=0, pady=8)
        self.symbolic_var_entry.insert(0, "x")
        
        input_content.columnconfigure(1, weight=1)
        
        # LaTeX 预览框
        preview_frame = ttk.LabelFrame(main_container, text="LaTeX 预览")
        preview_frame.pack(fill=tk.X, pady=(0, 15))
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 操作按钮框架
        button_frame = ttk.LabelFrame(main_container, text="操作")
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        button_content = ttk.Frame(button_frame)
        button_content.pack(fill=tk.X, padx=15, pady=15)
        
        button_container = ttk.Frame(button_content)
        button_container.pack(fill=tk.X)
        
        ttk.Button(button_container, text="求导", command=self.symbolic_differentiate, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_container, text="积分", command=self.symbolic_integrate, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_container, text="求解方程", command=self.symbolic_solve, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_container, text="傅里叶变换", command=self.symbolic_fourier, style='Modern.TButton').pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_container, text="保存到Excel", command=self.save_to_excel, style='Modern.TButton').pack(side=tk.LEFT)

        # 结果显示框架
        result_frame = ttk.LabelFrame(main_container, text="结果")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_content = ttk.Frame(result_frame)
        result_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.symbolic_result_text = tk.Text(result_content, 
                                          height=15,
                                          font=('Consolas', 10),
                                          bg='#f8f9fa',
                                          fg='#495057',
                                          borderwidth=1,
                                          relief='solid',
                                          selectbackground='#007bff',
                                          selectforeground='white')
        symbolic_scrollbar = ttk.Scrollbar(result_content, orient=tk.VERTICAL, command=self.symbolic_result_text.yview)
        self.symbolic_result_text.configure(yscrollcommand=symbolic_scrollbar.set)
        self.symbolic_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        symbolic_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_latex_preview(self, event=None):
        self.latex_preview.clear()
        expression = self.symbolic_expr_entry.get()
        try:
            self.latex_preview.text(0.5, 0.5, f'${expression}$', fontsize=12, ha='center', va='center')
        except Exception as e:
            self.latex_preview.text(0.5, 0.5, '无效的 LaTeX 公式', fontsize=12, ha='center', va='center')
        self.latex_preview.axis('off')
        self.canvas.draw()

    def symbolic_differentiate(self):
        """执行符号求导"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            try:
                _, latex_expr = self.main_window.symbolic_calc.latex_to_sympy(expression)
                if latex_expr is None:
                    raise ValueError
                result_str, result_expr = self.main_window.symbolic_calc.differentiate(str(latex_expr), variable)
            except Exception:
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
            self.main_window.append_to_current_data(result_data)
            
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
                
            try:
                _, latex_expr = self.main_window.symbolic_calc.latex_to_sympy(expression)
                if latex_expr is None:
                    raise ValueError
                result_str, result_expr = self.main_window.symbolic_calc.integrate_symbolic(str(latex_expr), variable)
            except Exception:
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
            self.main_window.append_to_current_data(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def symbolic_solve(self):
        """执行符号方程求解"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            try:
                _, latex_expr = self.main_window.symbolic_calc.latex_to_sympy(expression)
                if latex_expr is None:
                    raise ValueError
                result_str, result_expr = self.main_window.symbolic_calc.solve_equation(str(latex_expr), variable)
            except Exception:
                result_str, result_expr = self.main_window.symbolic_calc.solve_equation(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"方程: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"解: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '方程': [expression],
                '变量': [variable],
                '解': [result_str],
                '操作类型': ['符号求解']
            }
            self.main_window.append_to_current_data(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def symbolic_fourier(self):
        """执行傅里叶变换"""
        try:
            expression = self.symbolic_expr_entry.get()
            variable = self.symbolic_var_entry.get() or 'x'
            
            if not expression:
                messagebox.showwarning("输入错误", "请输入表达式")
                return
                
            try:
                _, latex_expr = self.main_window.symbolic_calc.latex_to_sympy(expression)
                if latex_expr is None:
                    raise ValueError
                result_str, result_expr = self.main_window.symbolic_calc.fourier_transform(str(latex_expr), variable)
            except Exception:
                result_str, result_expr = self.main_window.symbolic_calc.fourier_transform(expression, variable)
            
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"表达式: {expression}\n")
            self.symbolic_result_text.insert(tk.END, f"变量: {variable}\n")
            self.symbolic_result_text.insert(tk.END, f"傅里叶变换: {result_str}\n")
            
            # 保存结果到current_data
            result_data = {
                '原表达式': [expression],
                '变量': [variable],
                '傅里叶变换': [result_str],
                '操作类型': ['傅里叶变换']
            }
            self.main_window.append_to_current_data(result_data)
            
        except Exception as e:
            self.symbolic_result_text.delete(1.0, tk.END)
            self.symbolic_result_text.insert(tk.END, f"错误: {str(e)}")
    
    def save_to_excel(self):
        """保存符号计算结果到Excel"""
        if self.main_window.current_data is not None:
            self.main_window.save_excel_data()
        else:
            messagebox.showwarning("警告", "没有数据可保存，请先执行符号计算操作")