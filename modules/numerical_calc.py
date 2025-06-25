#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数值计算模块
功能：四则运算、数值积分、数值求解等
"""

import numpy as np
from scipy import integrate, optimize
# from scipy.misc import derivative  # 删除这行
from scipy.optimize import approx_fprime  # 添加这行
import math

class NumericalCalculator:
    def __init__(self):
        pass
    
    def basic_arithmetic(self, expression):
        """基本四则运算"""
        try:
            # 安全的数学表达式求值
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, 'det': np.linalg.det, 'inv': np.linalg.inv,
                'mat': np.matrix
            })
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return result
        except Exception as e:
            return f"错误: {str(e)}"
    
    def calculate_derivative(self, func, x_val, dx=1e-8):
        """计算函数在指定点的导数"""
        try:
            # 使用approx_fprime替代原来的derivative
            result = approx_fprime([x_val], lambda x: func(float(x)), dx)[0]
            return result
        except Exception as e:
            return f"错误: {str(e)}"
    
    def evaluate_expression(self, expression):
        """计算表达式 - 为GUI提供的接口"""
        return self.basic_arithmetic(expression)
    
    def numerical_derivative(self, func_str, variable, point):
        """数值求导 - 为GUI提供的接口"""
        try:
            def func(x):
                allowed_names = {
                    k: v for k, v in math.__dict__.items() if not k.startswith("__")
                }
                allowed_names[variable] = x
                return eval(func_str, {"__builtins__": {}}, allowed_names)
            
            return self.calculate_derivative(func, point)
        except Exception as e:
            return f"错误: {str(e)}"
    
    def solve_equation_numerical(self, func_str, variable='x', initial_guess=0):
        """数值求解方程 - 修复参数问题"""
        func_str = func_str.replace('^', '**')
        if '=' in func_str:
            func_str = '-'.join(map(lambda x: '('+x+')', func_str.split('=')))
        try:
            def func(x):
                allowed_names = {
                    k: v for k, v in math.__dict__.items() if not k.startswith("__")
                }
                allowed_names[variable] = x
                return eval(func_str, {"__builtins__": {}}, allowed_names)
            
            solution = optimize.fsolve(func, initial_guess)[0]
            return solution
        except Exception as e:
            return f"错误: {str(e)}"
    
    def numerical_integration(self, func_str, variable, a, b):
        """数值积分 - 为GUI提供的接口"""
        try:
            def func(x):
                allowed_names = {
                    k: v for k, v in math.__dict__.items() if not k.startswith("__")
                }
                allowed_names[variable] = x
                return eval(func_str, {"__builtins__": {}}, allowed_names)
            
            result, error = integrate.quad(func, a, b)
            return result
        except Exception as e:
            return f"错误: {str(e)}"
    
    def matrix_operations(self, operation, matrix1, matrix2=None):
        """矩阵运算"""
        try:
            mat1 = np.array(matrix1)
            
            if operation == "determinant":
                return np.linalg.det(mat1)
            elif operation == "inverse":
                return np.linalg.inv(mat1).tolist()
            elif operation == "eigenvalues":
                return np.linalg.eigvals(mat1).tolist()
            elif operation == "transpose":
                return mat1.T.tolist()
            elif operation == "add" and matrix2 is not None:
                mat2 = np.array(matrix2)
                return (mat1 + mat2).tolist()
            elif operation == "multiply" and matrix2 is not None:
                mat2 = np.array(matrix2)
                return np.dot(mat1, mat2).tolist()
            else:
                return "不支持的操作"
        except Exception as e:
            return f"错误: {str(e)}"