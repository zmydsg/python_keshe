#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
符号计算模块
功能：微积分计算、方程求解、傅里叶变换等
"""

import sympy as sp
from sympy import symbols, diff, integrate, solve, fourier_transform, inverse_fourier_transform
from sympy import sin, cos, exp, pi, oo, I
import numpy as np
from latex2sympy2 import latex2sympy

class SymbolicCalculator:
    def latex_to_sympy(self, latex_expr):
        try:
            sympy_expr = latex2sympy(latex_expr)
            return str(sympy_expr), sympy_expr
        except Exception as e:
            return f"错误: {str(e)}", None
            
    def __init__(self):
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.w = symbols('w', real=True)
    
    def differentiate(self, expression, variable='x', order=1):
        """求导数"""
        try:
            expr = sp.sympify(expression)
            var = symbols(variable)
            result = diff(expr, var, order)
            return str(result), result
        except Exception as e:
            return f"错误: {str(e)}", None
    
    def integrate_symbolic(self, expression, variable='x', limits=None):
        """符号积分"""
        try:
            expr = sp.sympify(expression)
            var = symbols(variable)
            
            if limits:
                # 定积分
                a, b = limits
                result = integrate(expr, (var, a, b))
            else:
                # 不定积分
                result = integrate(expr, var)
            
            return str(result), result
        except Exception as e:
            return f"错误: {str(e)}", None
    
    def solve_equation(self, equation, variable='x'):
        """求解方程"""
        try:
            eq = sp.sympify(equation)
            var = symbols(variable)
            solutions = solve(eq, var)
            return [str(sol) for sol in solutions], solutions
        except Exception as e:
            return [f"错误: {str(e)}"], None
    
    def fourier_transform(self, expression, variable='t', freq_var='w'):
        """傅里叶变换 - 为GUI提供的接口"""
        return self.fourier_transform_calc(expression, variable, freq_var)
    
    def fourier_transform_calc(self, expression, variable='t', freq_var='w'):
        """傅里叶变换"""
        try:
            expr = sp.sympify(expression)
            t_var = symbols(variable)
            w_var = symbols(freq_var)
            
            result = fourier_transform(expr, t_var, w_var)
            return str(result), result
        except Exception as e:
            return f"错误: {str(e)}", None
    
    def inverse_fourier_transform_calc(self, expression, freq_var='w', variable='t'):
        """逆傅里叶变换"""
        try:
            expr = sp.sympify(expression)
            w_var = symbols(freq_var)
            t_var = symbols(variable)
            
            result = inverse_fourier_transform(expr, w_var, t_var)
            return str(result), result
        except Exception as e:
            return f"错误: {str(e)}", None
    
    def simplify_expression(self, expression):
        """化简表达式"""
        try:
            expr = sp.sympify(expression)
            result = sp.simplify(expr)
            return str(result), result
        except Exception as e:
            return f"错误: {str(e)}", None