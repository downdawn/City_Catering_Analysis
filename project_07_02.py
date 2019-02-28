# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 21:40:44 2019

@author: Administrator
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

'''
(1) 加载数据
'''

import os
os.chdir(r'C:\Users\Administrator\Desktop\spyder\城市餐饮店铺选址分析')
df2 =pd.read_excel('空间统计.xlsx',sheetname=0)
df2.fillna(0,inplace = True)
df2.columns = ['人口密度','道路长度','餐饮计数','素菜餐饮计数','lng','lat']

'''
(2) 指标统计
'''

df2['rkmd_norm'] = (df2['人口密度']-df2['人口密度'].min())/(df2['人口密度'].max()-df2['人口密度'].min()) # 人口密度指标标准化
df2['cyrd_norm'] = (df2['餐饮计数']-df2['餐饮计数'].min())/(df2['餐饮计数'].max()-df2['餐饮计数'].min()) # 餐饮热度指标标准化
df2['tljp_norm'] = (df2['素菜餐饮计数'].max()-df2['素菜餐饮计数'])/(df2['素菜餐饮计数'].max()-df2['素菜餐饮计数'].min()) # 同类竞品指标标准化
df2['dlmi_norm'] = (df2['道路长度']-df2['道路长度'].min())/(df2['道路长度'].max()-df2['道路长度'].min()) # 道路密度指标标准化
# 指标标准化

df2['final_score'] = df2['rkmd_norm']*0.4 + df2['cyrd_norm']*0.3 + df2['tljp_norm']*0.1 + df2['dlmi_norm']*0.2
data_final_q2 = df2.sort_values(by = 'final_score',ascending=False).reset_index()
data_final_q2[:10]
# 计算综合评分并查看TOP10的网格ID

'''
(3) 制作空间散点图
'''
from bokeh.models import HoverTool

output_file('project07_h2.html')

data_final_q2['size'] = data_final_q2['final_score'] * 15
data_final_q2['color'] = 'green'
data_final_q2['color'].iloc[:10] = 'red'
# 添加size字段

source = ColumnDataSource(data_final_q2)
# 创建ColumnDataSource数据

hover = HoverTool(tooltips=[("经度", "@lng"),
                            ("纬度", "@lat"),
                            ("最终得分", "@final_score"),
                           ])  # 设置标签显示内容
p = figure(plot_width=800, plot_height=800,
                title="空间散点图" , 
                tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair']) 
# 构建绘图空间

p.square(x = 'lng',y = 'lat',source = source,
         line_color = 'black',fill_alpha = 0.5,
        size = 'size',color = 'color')
p.ygrid.grid_line_dash = [6, 4]
p.xgrid.grid_line_dash = [6, 4]
# 散点图
show(p)



print('finashed')