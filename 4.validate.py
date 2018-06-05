# -*- coding: utf-8 -*-

import pandas as pd
import utils

one_hot_df = pd.read_csv('one_hot_df.csv')
data = pd.read_csv(open('classical.csv'))
cluster = utils.load_pickle('cluster.txt')
list_name = utils.load_pickle('list_name.txt')
length = len(cluster)
length_2 = one_hot_df.shape[0]

item_list = []
l2 = []

index_list = []
for i in range(length):
    item = cluster[i]
    if item != []:
        item[0].insert(0, list_name[i])
        item_list.append(sorted(item[0]))

[l2.append(i) for i in item_list if i not in l2]

'''
[['人参', '当归', '炙甘草', '白术'],
 ['仙茅', '巴戟天', '淫羊藿', '知母'],
 ['大怀熟地', '山茱萸', '枸杞', '菟丝子'],
 ['制何首乌', '牛膝', '酒浸当归', '酒浸枸杞子']]

'''
for n in range(length_2):
    index = []
    for item in l2:
        flag = 1
        for i in item:
            column = one_hot_df[i]
            if column[n] == 0:
                flag = 0
                break
        if flag == 1:
            index.append(n)
            index_list.append([item.copy(), index])

    

'''
[[['人参', '当归', '炙甘草', '白术'], [10]],
 [['人参', '当归', '炙甘草', '白术'], [14]],
 [['人参', '当归', '炙甘草', '白术'], [18]],
 [['人参', '当归', '炙甘草', '白术'], [24]],
 [['大怀熟地', '山茱萸', '枸杞', '菟丝子'], [26]],
 [['仙茅', '巴戟天', '淫羊藿', '知母'], [30]],
 [['制何首乌', '牛膝', '酒浸当归', '酒浸枸杞子'], [33]]]
'''
for item in index_list:
    item.append(data['证型'][item[-1][0]])
    #item.append(data['功用大类'][item[-1][0]])


# =============================================================================
# l2 = [['人参', '当归', '炙甘草', '白术'],
#  ['大怀熟地', '山茱萸', '枸杞', '菟丝子'],
#  ['仙茅', '巴戟天', '淫羊藿', '知母'],
#  ['制何首乌', '牛膝', '酒浸当归', '酒浸枸杞子']]
# index_list[0][-1] = '血虚证'
# set_point = 0
# set_point_2 = 0
# for n in l2[set_point:]:
#     i = 0
#     i_list = []
#     max_count = 0
#     for item in index_list[set_point_2:]:
#         if item[0] == n:
#             i += 1
#             set_point_2 += 1
#             i_list.append(item[-1])
#             print(item[0], n, set_point_2)
#         else:
#             break
#     set_point += 1
#     i_set = set(i_list)
#     for q in i_set:
#         if max_count < i_list.count(q):
#             max_count = i_list.count(q)
#     n.append([i, max_count])
# =============================================================================
for n in l2:
    i = 0
    i_list = []
    max_count = 0
    for item in index_list:
        if item[0] == n:
            i += 1
            i_list.append(item[-1])
    i_set = set(i_list)
    for q in i_set:
        if max_count < i_list.count(q):
            max_count = i_list.count(q)
        
    n.append([i, max_count])
    
        

                
            
                
        
