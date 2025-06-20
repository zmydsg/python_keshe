import pandas as pd
import numpy as np
from openpyxl import Workbook
import os

class ExcelHandler:
    def __init__(self):
        pass
    
    def read_excel(self, file_path, sheet_name=0, chunk_size=None, usecols=None):
        """读取Excel文件
        
        参数:
            file_path: Excel文件路径
            sheet_name: 工作表名称或索引
            chunk_size: 分块读取的行数，用于大文件
            usecols: 只读取指定的列
        """
        try:
            if chunk_size:
                # 分块读取大文件
                chunks = pd.read_excel(file_path, sheet_name=sheet_name, 
                                      usecols=usecols, chunksize=chunk_size)
                return chunks  # 返回迭代器，供后续处理
            else:
                df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=usecols)
                return df
        except Exception as e:
            return f"读取Excel文件错误: {str(e)}"
    
    def write_excel(self, data, file_path, sheet_name='Sheet1', mode='w'):
        """写入Excel文件
        
        参数:
            data: 要写入的数据
            file_path: 保存路径
            sheet_name: 工作表名称
            mode: 'w'表示覆盖，'a'表示追加
        """
        try:
            if isinstance(data, dict):
                df = pd.DataFrame(data)
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = data
            
            if mode == 'a' and os.path.exists(file_path):
                with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                df.to_excel(file_path, sheet_name=sheet_name, index=False)
                
            return f"数据已保存到 {file_path}"
        except Exception as e:
            return f"写入Excel文件错误: {str(e)}"
    
    def get_column_data(self, df, column_name):
        """获取指定列数据"""
        try:
            if column_name in df.columns:
                return df[column_name].dropna().tolist()
            else:
                return f"列 '{column_name}' 不存在"
        except Exception as e:
            return f"获取列数据错误: {str(e)}"
    
    def get_sheet_names(self, file_path):
        """获取Excel文件中的工作表名称"""
        try:
            xl_file = pd.ExcelFile(file_path)
            return xl_file.sheet_names
        except Exception as e:
            return f"获取工作表名称错误: {str(e)}"
    
    def get_numeric_columns(self, df):
        """获取数值型列名"""
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    def get_text_columns(self, df):
        """获取文本型列名"""
        return df.select_dtypes(include=['object']).columns.tolist()
    
    def export_column_to_list(self, df, column_name):
        """将指定列导出为列表，用于其他模块计算"""
        try:
            if column_name in df.columns:
                return df[column_name].dropna().tolist()
            else:
                return []
        except Exception as e:
            return []