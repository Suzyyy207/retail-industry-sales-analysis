import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from scipy.stats import boxcox
from sklearn.cluster import KMeans
from prettytable import PrettyTable
from scipy.stats import pointbiserialr
from sklearn.metrics import silhouette_score

raw_df = pd.read_csv('./Data/full_name_all_feature_with_label.csv')

def get_df(raw_df):
    num_df = {}
    not_used = ['name','profit','sell_count','profit_money','label']
    for key in raw_df.keys():
        if key not in not_used:
            num_df[key] = []
    for i in range(len(raw_df['name'])):
        num_df['maker'].append(raw_df['maker'][i])
        num_df['deliver_time'].append(raw_df['deliver_time'][i])
        num_df['deliver_way'].append(raw_df['deliver_way'][i])
        num_df['discount'].append(raw_df['discount'][i])
        num_df['category'].append(raw_df['category'][i])
        num_df['sub_category'].append(raw_df['sub_category'][i])
        num_df['price'].append(raw_df['price'][i])
        num_df['main_user'].append(raw_df['main_user'][i])
        num_df['area_div'].append(raw_df['area_div'][i])
        num_df['province_div'].append(raw_df['province_div'][i])
        num_df['city_div'].append(raw_df['city_div'][i])
    return num_df

df = pd.DataFrame(data=get_df(raw_df))

boundary={}
cluster_table=PrettyTable()
labels=["parameter", "total"]
cluster_table.field_names = labels
param_distribute_list = ['price','discount','area_div','province_div','city_div','deliver_time','deliver_way']
kmeans_result_3 = []
kmeans_result_4 = []
kmeans_result_5 = []
score = {'price':{'n_cluster=3':0,'n_cluster=4':0,'n_cluster=5':0},
         'discount':{'n_cluster=3':0,'n_cluster=4':0,'n_cluster=5':0},
         'area_div':{'n_cluster=3':0,'n_cluster=4':0,'n_cluster=5':0},
         'province_div':{'n_cluster=3':0,'n_cluster=4':0,'n_cluster=5':0},
         'city_div':{'n_cluster=3':0,'n_cluster=4':0,'n_cluster=5':0}
        }


# 离散化
n_clusters=3
labels.extend([i for i in range(n_clusters)])

fig,axs=plt.subplots(nrows=2,ncols=3,figsize=(12,12))

for i in range(7):
    row=i//3
    col=i%3
    ax=axs[row][col]
    param=param_distribute_list[i]
    temp=np.array(df[param].values.reshape(-1, 1)).reshape(-1,1)
    kmeans=KMeans(n_clusters=n_clusters).fit(temp)
    result=kmeans.predict(temp)
    #kmeans_result_3.append(result)
    silhouette_avg = silhouette_score(temp, result)
    score[param]['n_cluster=3'] = silhouette_avg
    counts=np.bincount(kmeans.labels_) 
    centers=kmeans.cluster_centers_
    boundary[param]=[item[0] for item in centers]
    boundary[param].sort()
    total=sum(counts)
    row=[param,total]
    #for j in range(len(counts)):
    #    row.append('{}({}%)'.format(centers[j],round(counts[j]/total*100,1)))
    #cluster_table.add_row(row)
    ax.scatter(result,temp)
    ax.set_title(param)
plt.tight_layout()
plt.show()

#print(cluster_table)