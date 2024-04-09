import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from sklearn.cluster import KMeans
from prettytable import PrettyTable

raw_df = pd.read_csv('./Data/deal_add_all_below_10.csv')

# 编码
# 编码
deliver_way_dict = {'当日': 1, '一级': 2, '二级': 3, '标准级': 4}
category_dict = {'办公用品': 1, '技术':2, '家具': 3}
type_dict = {'消费者':0, '小型企业':1, '公司':2 }

sub_category_dict = {}
item_set = set()
for item in raw_df['sub_category']:
    if item not in item_set:
        sub_category_dict[item] = len(item_set) + 1
        item_set.add(item)

brand_dict = {}
item_set = set()
for item in raw_df['brand']:
    if item not in item_set:
        brand_dict[item] = len(item_set) + 1
        item_set.add(item)
        
area_dict = {
    '华北': 1,
    '东北': 2,
    '华东': 3, 
    '中南': 3, 
    '西南': 5, 
    '西北': 6
}

location_dict = {'华北': {},'东北': {},'华东': {},'中南': {}, '西南': {}, '西北': {}}

for i in range(len(raw_df['name'])):
    area = raw_df['user_area'][i]
    province = raw_df['user_province'][i]
    city = raw_df['user_city'][i]
    if province not in location_dict[area].keys():
        location_dict[area][province] = {}
    location_dict[area][province][city] = 0

province_dict = {}
city_dict = {}

for key in location_dict.keys():
    p_dict = location_dict[key]
    count = 0
    for province in p_dict.keys():
        province_dict[province] = eval(str(area_dict[key]) + str(count))
        count += 1
    for province in p_dict.keys():
        c_dict = location_dict[key][province]
        count = 0
        for city in c_dict.keys():
            if count < 10:
                cnt_str = str('00') + str(count)
            elif count < 100:
                cnt_str = str('0') + str(count)
            city_dict[city] = eval(str(area_dict[key]) + str(province_dict[province]) + cnt_str)
            count += 1

            
def get_feature(raw_df):
    features = []
    labels = []
    for i in range(len(raw_df['name'])):
        feature = []
        feature.append(brand_dict[raw_df['brand'][i]])
        feature.append(raw_df['days'][i])
        feature.append(deliver_way_dict[raw_df['deliver_way'][i]])
        feature.append(raw_df['discount'][i])
        feature.append(category_dict[raw_df['category'][i]])
        feature.append(sub_category_dict[raw_df['sub_category'][i]])
        feature.append(raw_df['price'][i])
        feature.append(type_dict[raw_df['user_type'][i]])
        feature.append(city_dict[raw_df['user_city'][i]])
        feature.append(province_dict[raw_df['user_province'][i]])
        feature.append(area_dict[raw_df['user_area'][i]])
        
        features.append(feature)
        labels.append(raw_df['label'][i])
    
    return features,labels


def get_df(raw_df):
    num_df = {}
    for key in raw_df.keys():
        if key != 'label' and key != 'name':
            num_df[key] = []
    for i in range(len(raw_df['name'])):
        num_df['brand'].append(brand_dict[raw_df['brand'][i]])
        num_df['days'].append(raw_df['days'][i])
        num_df['deliver_way'].append(deliver_way_dict[raw_df['deliver_way'][i]])
        num_df['discount'].append(raw_df['discount'][i])
        num_df['category'].append(category_dict[raw_df['category'][i]])
        num_df['sub_category'].append(sub_category_dict[raw_df['sub_category'][i]])
        num_df['price'].append(raw_df['price'][i])
        num_df['user_type'].append(type_dict[raw_df['user_type'][i]])
        num_df['user_city'].append(city_dict[raw_df['user_city'][i]])
        num_df['user_province'].append(province_dict[raw_df['user_province'][i]])
        num_df['user_area'].append(area_dict[raw_df['user_area'][i]])
        num_df['profit'].append(raw_df['profit'][i])
        num_df['sell_num'].append(raw_df['sell_num'][i])
    return num_df

features,labels = get_feature(raw_df)
df = pd.DataFrame(data=get_df(raw_df))

n_clusters=3

boundary={}
cluster_table=PrettyTable()
labels=["parameter", "total"]
labels.extend([i for i in range(n_clusters)])
cluster_table.field_names = labels
param_distribute_list = ['price','discount','sell_num']

fig,axs=plt.subplots(nrows=2,ncols=2,figsize=(12,12))

for i in range(3):
    row=i//2
    col=i%2
    ax=axs[row][col]
    param=param_distribute_list[i]
    temp=np.array(df[param].values.reshape(-1, 1)).reshape(-1,1)
    kmeans=KMeans(n_clusters=3).fit(temp)
    result=kmeans.predict(temp)
    counts=np.bincount(kmeans.labels_) 
    centers=kmeans.cluster_centers_
    boundary[param]=[item[0] for item in centers]
    boundary[param].sort()
    total=sum(counts)
    row=[param,total]
    for j in range(len(counts)):
        row.append('{}({}%)'.format(centers[j],round(counts[j]/total*100,1)))
    cluster_table.add_row(row)
    ax.scatter(result,temp)
    ax.set_title(param)
plt.tight_layout()
plt.show()