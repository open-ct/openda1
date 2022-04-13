import pandas as pd
from pyecharts.charts import HeatMap
from pyecharts import options as opts
from pyecharts.faker import Faker
import numpy as np
import random

f = pd.read_csv("join3.csv")

mymap = [[i, j, 0] for i in range(3) for j in range(5)]
mymap2 = [[i, j, 0] for i in range(3) for j in range(5)]

i = 0
for index in f.index:
    for i, value in enumerate(eval(f.loc[index, 'answer'])):
        value = eval(value)
        mymap2[value[0]*5 + value[1]][2] += 1
        if i == 0 and value[0] == 0 and value[1] == 0:
            continue
        mymap[value[0]*5 + value[1]][2] += 1
print(mymap)
x_axis = ['0', '1', '2']

y_axis = [
    '0', '1', '2', '3', '4'
]
# heatmap = HeatMap()
# heatmap.add_xaxis('热力图', x_axis, y_axis, mymap, is_visualmap=True, visual_range=[10000, 25000], visual_range_color=['#FFF', '#FF0000'], visual_range_text=[
#     'less', 'more'], visual_pos='center', visual_split_number=10, visual_text_color="#000", visual_orient="horizontal", tooltip_formatter='{c}')

# heatmap.render("./html/heatmap_base.html")

hm = HeatMap()
hm.add_xaxis(x_axis)
hm.add_yaxis("", y_axis, mymap)
hm.set_global_opts(
    title_opts=opts.TitleOpts(title="冰箱-热力图"),
    visualmap_opts=opts.VisualMapOpts(
        min_=0, max_=9000,
        range_color=['#FFF', "#FF0000"],
        split_number=10,
        orient="horizontal",  # 视觉映射组件水平放置
        pos_left="center"))  # 居中
hm.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
hm.render("./html/heatmap_label11.html")


hm = HeatMap()
hm.add_xaxis(x_axis)
hm.add_yaxis("", y_axis, mymap2)
hm.set_global_opts(
    title_opts=opts.TitleOpts(title="冰箱-热力图"),
    visualmap_opts=opts.VisualMapOpts(
        min_=0, max_=9000,
        range_color=['#FFF', "#FF0000"],
        split_number=10,
        orient="horizontal",  # 视觉映射组件水平放置
        pos_left="center"))  # 居中
hm.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside"))
hm.render("./html/heatmap_label22.html")
