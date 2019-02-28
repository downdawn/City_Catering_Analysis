# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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
df1 =pd.read_excel('上海餐饮数据.xlsx',sheetname=0)

'''
(2) 计算口味，人均消费，性价比指标
'''

data1 = df1[['类别','口味','环境','服务','人均消费']]
data1.dropna(inplace = True)
data1 = data1[(data1['口味']>0)&(data1['人均消费']>0)]
# 筛选数据，清除空值、为0的数据

data1['性价比'] = (data1['口味'] + data1['环境'] + data1['服务']) / data1['人均消费']
# 计算性价比指数

def f1():
    fig,axes = plt.subplots(1,3,figsize = (10,4))
    data1.boxplot(column = ['口味'], ax = axes[0])
    data1.boxplot(column = ['人均消费'], ax = axes[1])
    data1.boxplot(column = ['性价比'], ax = axes[2])
# 函数1：制作箱线图，查看异常值

def f2(data,col):
    q1 = data[col].quantile(q = 0.25)
    q3 = data[col].quantile(q = 0.75) 
    iqr = q3-q1
    t1 = q1 - 3 * iqr
    t2 = q3 + 3 * iqr
    return data[(data[col] > t1)&(data[col]<t2)][['类别',col]]
# 函数2： 清除异常值
    
data_kw = f2(data1,'口味')
data_rj = f2(data1,'人均消费')
data_xjb = f2(data1,'性价比')

def f3(data,col):
    col_name = col + '_norm'
    data_gp = data.groupby('类别').mean()
    data_gp[col_name] = (data_gp[col] - data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by = col_name, inplace = True, ascending=False)
    return data_gp
# 函数3：标准化指标并排序，区间[0,1]

data_kw_score = f3(data_kw,'口味')
data_rj_score = f3(data_rj,'人均消费')
data_xjb_score = f3(data_xjb,'性价比')
# 指标标准化得分

data_final_q1 = pd.merge(data_kw_score,data_rj_score,left_index=True,right_index=True)    # 合并口味、人均消费指标得分
data_final_q1 = pd.merge(data_final_q1,data_xjb_score,left_index=True,right_index=True)       # 合并性价比指标得分
# 合并数据

'''
(3) 绘制图表辅助分析
'''

from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.models.annotations import BoxAnnotation

output_file('project07_h1.html')

data_final_q1['size'] = data_final_q1['口味_norm'] * 40
data_final_q1.index.name = 'type'
data_final_q1.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']
# 将中文改为英文(建议)
# 添加颜色参数size

source = ColumnDataSource(data_final_q1)
# 创建数据

hover = HoverTool(tooltips=[("餐饮类型", "@type"),
                            ("人均消费", "@price"),
                            ("性价比得分", "@xjb_norm"),
                            ("口味得分", "@kw_norm")
                           ])  # 设置标签显示内容

result = figure(plot_width=800, plot_height=300, title="餐饮类型得分情况" ,
                x_axis_label = '人均消费', y_axis_label = '性价比得分', 
                tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair']
                ) 

result.circle(x = 'price',y = 'xjb_norm', source = source,
              line_color = 'black', line_dash = [6,4], fill_alpha = 0.6, size = 'size')
# 绘制散点图
price_mid = BoxAnnotation(left=40,right=80, fill_alpha=0.1, fill_color='navy')   
result.add_layout(price_mid)
# 设置人均消费中间价位区间

data_type = data_final_q1.index.tolist()  # 提取横坐标

kw = figure(plot_width=800, plot_height=300, title="口味得分" ,
            x_range = data_type,
            tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
kw.vbar(x = 'type', top = 'kw_norm',source = source,
        width = 0.8, alpha = 0.7, color = 'red')
# 柱状图1

price = figure(plot_width=800, plot_height=300, title="人均消费得分" ,
            x_range = data_type,
            tools=[hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
price.vbar(x = 'type', top = 'price_norm',source = source,
        width = 0.8, alpha = 0.7, color = 'green')
# 柱状图2

p = gridplot([[result],[kw],[price]])
# 组合图表

show(p)


print('finashed')