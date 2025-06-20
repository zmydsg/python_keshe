#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据处理模块
功能：统计分析、曲线拟合等
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
# Fix the import for PolynomialFeatures
from sklearn.preprocessing import PolynomialFeatures  # Changed from sklearn.polynomial

class DataProcessor:
    def __init__(self):
        pass
    
    def basic_statistics(self, data):
        """基本统计分析"""
        try:
            data = np.array(data)
            stats_dict = {
                '均值': np.mean(data),
                '中位数': np.median(data),
                '标准差': np.std(data),
                '方差': np.var(data),
                '最小值': np.min(data),
                '最大值': np.max(data),
                '四分位数': np.percentile(data, [25, 50, 75]).tolist()
            }
            return stats_dict
        except Exception as e:
            return f"错误: {str(e)}"
    
    def correlation_analysis(self, x_data, y_data):
        """相关性分析"""
        try:
            correlation, p_value = stats.pearsonr(x_data, y_data)
            return {
                '相关系数': correlation,
                'p值': p_value,
                '相关性强度': self._interpret_correlation(correlation)
            }
        except Exception as e:
            return f"错误: {str(e)}"
    
    def _interpret_correlation(self, corr):
        """解释相关性强度"""
        abs_corr = abs(corr)
        if abs_corr >= 0.8:
            return "强相关"
        elif abs_corr >= 0.5:
            return "中等相关"
        elif abs_corr >= 0.3:
            return "弱相关"
        else:
            return "几乎无相关"
    
    def curve_fitting(self, x_data, y_data, fit_type='linear'):
        """曲线拟合"""
        try:
            x_data = np.array(x_data)
            y_data = np.array(y_data)
            
            if fit_type == 'linear':
                # 线性拟合
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
                fitted_y = slope * x_data + intercept
                equation = f"y = {slope:.4f}x + {intercept:.4f}"
                r_squared = r_value ** 2
                
            elif fit_type == 'polynomial':
                # 多项式拟合（二次）
                coeffs = np.polyfit(x_data, y_data, 2)
                fitted_y = np.polyval(coeffs, x_data)
                equation = f"y = {coeffs[0]:.4f}x² + {coeffs[1]:.4f}x + {coeffs[2]:.4f}"
                r_squared = self._calculate_r_squared(y_data, fitted_y)
                
            elif fit_type == 'exponential':
                # 指数拟合
                def exp_func(x, a, b, c):
                    return a * np.exp(b * x) + c
                
                popt, _ = curve_fit(exp_func, x_data, y_data, maxfev=1000)
                fitted_y = exp_func(x_data, *popt)
                equation = f"y = {popt[0]:.4f} * exp({popt[1]:.4f}x) + {popt[2]:.4f}"
                r_squared = self._calculate_r_squared(y_data, fitted_y)
            
            return {
                '拟合方程': equation,
                '拟合数据': fitted_y.tolist(),
                'R²': r_squared,
                '拟合类型': fit_type
            }
            
        except Exception as e:
            return f"错误: {str(e)}"
    
    def _calculate_r_squared(self, y_actual, y_predicted):
        """计算R²值"""
        ss_res = np.sum((y_actual - y_predicted) ** 2)
        ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
        return 1 - (ss_res / ss_tot)
    
    def outlier_detection(self, data, method='iqr'):
        """异常值检测"""
        try:
            data = np.array(data)
            
            if method == 'iqr':
                Q1 = np.percentile(data, 25)
                Q3 = np.percentile(data, 75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = data[(data < lower_bound) | (data > upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(data))
                outliers = data[z_scores > 3]
            
            return {
                '异常值': outliers.tolist(),
                '异常值数量': len(outliers),
                '检测方法': method
            }
            
        except Exception as e:
            return f"错误: {str(e)}"