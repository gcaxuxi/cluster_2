# -*- coding: utf-8 -*-
#from treat import *
import re
import pandas as pd
import numpy as np
import itertools
import utils 

#1.1 初步清洗目标列的数据，并返回
def preprocess(column_name, data):
    for i in range(length):
        item = data[column_name].loc[i]
        if column_name == '处方（处理）':
            item = re.sub(r'\S钱', '', item)
        item = re.sub(r'[\或\以及]', '', item)
        pre = re.sub(r'\（.*?\）|{.*?\}', '', item)
        pre = re.split(r'[\d\．\！\……\。\；\，\,]', pre)
        pre = [x for x in pre if x != '']
        data[column_name].loc[i] = pre
    return data

#1.2 判断每一条数据的长度，这里阈值设为5；过长的数据打印出来，由此设置manual_process(人工处理)
def check(name, data):
    for i in range(length):
        item = data[name][i]
        for n in item:
            if len(n) > 5:
                print(n, i, item)
                print('-'*50)

def manual_process(name, data):
    data[name][16][0] = '桃仁'
    data[name][16].append('红花')
    data[name][33][-1] = '补骨脂'
    data[name][51][0] = '川芎'
    data[name][51][1:] = ['阿胶', '甘草', '艾叶', '当归', '芍药', '干地黄']
    return data

#2.1 计算方剂所报含的所有药物各自的频率，以字典保存
def count_dic(column_name, data_length, data):
    count_dic = {}
    for i in range(data_length):
        for per in data[column_name][i]:
            count_dic[per] = (count_dic[per] if per in count_dic else 0) + 1
    return count_dic

#2.2 按value排列字典，这里指频率降序排列药物，并将药物名称和频率保存各自保存到list     
def dic_list(dic):
    list_name, list_frequecy =  [], []
    reversed_list = sorted(dic.items(),key = lambda x:x[1],reverse = True)
    for i in reversed_list:
        list_name.append(i[0])
        list_frequecy.append(i[-1])
    return list_name, list_frequecy
    
# 3. 生成关于药物的one-hot，即每条药方根据药物有无 标 1or0
def one_hot(list_name, input_data, column_name = '处方（处理）'):
    df = pd.DataFrame(np.zeros((length, len(list_name))), columns= list_name)
    for i in range(length):
        for name in input_data[column_name].loc[i]:
            df[name].loc[i] = 1
    return df

# 4. 药物两两组合，计算组合频率，返回字典格式
def combinations_dic(data_length, input_list_name, one_hot_data):
    combinations = list(itertools.combinations(range(len(input_list_name)),2))
    combinations_fre = {}
    for i in range(data_length):
        for item in combinations:
            pre, suf = item
            if one_hot_data[input_list_name[pre]][i] == 1 and one_hot_data[input_list_name[suf]][i] == 1:
                combinations_fre[item] = (combinations_fre[item] if item in combinations_fre else 0) + 1 
    return combinations_fre


if __name__ == "__main__":
    data = pd.read_csv(open('classical.csv'))
    length = data.shape[0]  
    data = preprocess('处方（处理）', data)
    check('处方（处理）', data)
    data = manual_process('处方（处理）', data)
    
    count_dic = count_dic('处方（处理）', length, data)
    list_name, list_frequency = dic_list(count_dic) #l1药物名:168，list_frequecy频数:474
    one_hot_df = one_hot(list_name, data)
    one_hot_df.to_csv('one_hot_df.csv', index = False, encoding = 'utf-8')
    combinations_dic_fre = combinations_dic(length, list_name, one_hot_df)
    combinations_list, combinations_frequency = dic_list(combinations_dic_fre) #l3药物组合index，l4频数
    list_fre = [i/sum(list_frequency) for i in list_frequency]
    combinations_fre = [i/sum(list_frequency) for i in combinations_frequency]
    

    utils.save_pickle('list_name.txt', list_name)
    utils.save_pickle('list_fre.txt', list_fre)
    utils.save_pickle('combinations_list.txt', combinations_list)
    utils.save_pickle('combinations_fre.txt', combinations_fre)

# =============================================================================
#     list_1 = []
#     for item in data['处方（处理）']:
#         list_1.append(item)
#     utils.save_pickle('data.txt', list_1)
# =============================================================================

    
    
    
    
