#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科学计算工具 - 主程序
功能：符号计算、数值计算、数据处理、可视化、GUI界面
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import ScientificCalculatorGUI

def main():
    """主函数"""
    app = ScientificCalculatorGUI()
    app.run()

if __name__ == "__main__":
    main()