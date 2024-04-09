import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import Map
from pyecharts import options as opts
import squarify
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号

df = pd.read_excel('./超市.xls')
city = ['北京','上海','重庆','天津']
self_domain = ['内蒙古','广西','西藏','新疆','宁夏']
self_name = ['内蒙古自治区','广西壮族自治区','西藏自治区','新疆维吾尔自治区','宁夏回族自治区']

row, col = df.shape  #获取excel文件中除第一行外的行和列数

province = {} # 各省份的订单量
province_time = {} # 各省份不同年度的订单量
profit = {}
profit_time = {}
region = {}
catagory = {}

# 统计各省份的消费群体属于公司、消费者以及小型企业的数量
province_company = {}
province_customer = {}
province_enterprice = {}

# 统计各省份的消费类别属于办公用品、家具以及技术的数量
province_work = {}
province_tech = {}
province_house = {}

# 处理表格数据
for i in range(row):
    time = int( str(df['订单日期'][i])[0:4] )
    m = str( df['利润'][i] )
    if len( m.split(',') ) == 1:
        m = int(m)
    else:
        m = int( m.split(',')[0] + m.split(',')[1] )
        
    if df['省/自治区'][i] not in province: 
        province[ df['省/自治区'][i] ] = 1
        province_time[ df['省/自治区'][i] ] = [0,0,0,0]
        province_time[ df['省/自治区'][i] ][ time-2013 ] = 1  #2013年对应下标0位置
        profit[ df['省/自治区'][i] ] = m
        profit_time[ df['省/自治区'][i] ] = [0,0,0,0]
        profit_time[ df['省/自治区'][i] ][ time-2013 ] = m
        
        if df['地区'][i] not in region:
            region[ df['地区'][i] ] = []
        region[ df['地区'][i] ].append( df['省/自治区'][i] )
        
        if df['细分'][i] == '公司':
            province_company[ df['省/自治区'][i] ] = 1
        elif df['细分'][i] == '消费者':
            province_customer[ df['省/自治区'][i] ] = 1
        else:
            province_enterprice[ df['省/自治区'][i] ] = 1
            
        if df['类别'][i] == '办公用品':
            province_work[ df['省/自治区'][i] ] = 1
        elif df['类别'][i] == '技术':
            province_tech[ df['省/自治区'][i] ] = 1
        else:
            province_house[ df['省/自治区'][i] ] = 1
            
            
    else: 
        province[ df['省/自治区'][i] ] += 1
        province_time[ df['省/自治区'][i] ][ time-2013 ] += 1
        profit[ df['省/自治区'][i] ] += m
        profit_time[ df['省/自治区'][i] ][ time-2013 ] += m
        
        if df['细分'][i] == '公司':
            if df['省/自治区'][i] not in province_company:
                province_company[ df['省/自治区'][i] ] = 1
            else:
                province_company[ df['省/自治区'][i] ] += 1
        elif df['细分'][i] == '消费者':
            if df['省/自治区'][i] not in province_customer:
                province_customer[ df['省/自治区'][i] ] = 1
            else:
                province_customer[ df['省/自治区'][i] ] += 1
        else:
            if df['省/自治区'][i] not in province_enterprice:
                province_enterprice[ df['省/自治区'][i] ] = 1
            else:
                province_enterprice[ df['省/自治区'][i] ] += 1
            
            
        if df['类别'][i] == '办公用品':
            if df['省/自治区'][i] not in province_work:
                province_work[ df['省/自治区'][i] ] = 1
            else:
                province_work[ df['省/自治区'][i] ] += 1
        elif df['类别'][i] == '技术':
            if df['省/自治区'][i] not in province_tech:
                province_tech[ df['省/自治区'][i] ] = 1
            else:
                province_tech[ df['省/自治区'][i] ] += 1
        else:
            if df['省/自治区'][i] not in province_house:
                province_house[ df['省/自治区'][i] ] = 1
            else:
                province_house[ df['省/自治区'][i] ] += 1
                
    if df['子类别'][i] not in catagory:
        catagory[ df['子类别'][i] ] = 1
    else:
        catagory[ df['子类别'][i] ] += 1
        
# 统计各省份的消费类别属于办公用品、家具以及技术的情况
classification = ['办公用品','技术','家具']
work = []
tech = []
house = []
for each in province_work.keys():
    work.append(province_work[each])
    house.append(province_house[each])
    if each == '西藏':
        tech.append(0)
    else:
        tech.append(province_tech[each])

province_index = np.repeat( list(province_work.keys()),3 )  #3个商品类别
classification_column = classification * len(province_work.keys())
work_tech_house = []
for i in range( len(province_work.keys()) ):
    work_tech_house.append(work[i])
    work_tech_house.append(tech[i])
    work_tech_house.append(house[i])
df_p = pd.DataFrame({'省份':province_index,'类别':classification_column,'数值':work_tech_house})
df_wide = df_p.pivot_table( index = '省份', columns = '类别', values = '数值' )

fig,ax = plt.subplots(figsize = (12,12))
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
sns.heatmap(
    df_wide,
annot = True,
    cmap = "YlGnBu",
    linecolor = 'white',
    linewidths = 0.5
)
plt.title('各省份的消费类别')
plt.savefig('./hi.jpg')
plt.show()
