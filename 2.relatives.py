# -*- coding: utf-8 -*-
import pandas as pd
from math import log
import utils

def comb_names(list_name):
    combinations_name = [] #组合药物名
    for i in combinations_list:
        pre, suf = i
        combinations_name.append([list_name[pre], list_name[suf]])
    return combinations_name
    
def calculate_correlation(combinations_list, combinations_fre, list_fre):
    correlation = []   #关联度系数
    for i in range(len(combinations_list)):
        flag_1, flag_2, flag_3 = 1, 1, 1
        pre, suf = combinations_list[i]
        H_pre = -list_fre[pre] * log(list_fre[pre]) - (1- list_fre[pre]) * log((1- list_fre[pre]))
        H_suf = -list_fre[suf] * log(list_fre[suf]) - (1- list_fre[suf]) * log((1- list_fre[suf]))
        param_1 = list_fre[pre] - combinations_fre[i]
        param_2 = list_fre[suf] - combinations_fre[i]
        param_3 = 1 + combinations_fre[i] - list_fre[pre] -list_fre[suf]
        if param_1 ==0:
            flag_1 = 0
            param_1 = 1
        if param_2 ==0:
            flag_2 = 0
            param_2 = 1
        if param_3 ==0:
            flag_3 = 0
            param_3 = 1
        H_pre_suf = -combinations_fre[i] * log(combinations_fre[i]) - flag_1 * param_1 * log(param_1) - flag_2 * param_2 * log(param_2) - flag_3 * param_3 * log(param_3)
        result = H_pre + H_suf - H_pre_suf
        #result = combinations_fre[i] * log(combinations_fre[i]/(list_fre[pre]*list_fre[suf]))
        correlation.append(result)
    return correlation

def relatives(list_name, data, relatives_num):
    relatives_list = []   #药物亲友团
    length = data.shape[0]
    for item in list_name:
        list_ = []
        for i in range(length):
            if item in data['药物'][i]:
                list_.append(data['药物'][i])
        relatives_list.append(list_)
    def limited_relatives(input_list, relatives_num):
        result = []
        for i in range(len(input_list)):
            if len(input_list[i]) >= relatives_num:
                result.append(input_list[i][:relatives_num])
            else:
                result.append(input_list[i])
        return result
    return limited_relatives(relatives_list, relatives_num)       


if __name__ == "__main__":
    list_name = utils.load_pickle('list_name.txt')
    list_fre = utils.load_pickle('list_fre.txt')
    combinations_list = utils.load_pickle('combinations_list.txt')
    combinations_fre = utils.load_pickle('combinations_fre.txt')
    correlation = calculate_correlation(combinations_list, combinations_fre, list_fre)
    combinations_name = comb_names(list_name)
    column_1 = pd.Series(combinations_name, name='药物')  
    column_2 = pd.Series(correlation, name='关联度系数')  
    data = pd.concat([column_1, column_2], axis=1)  
    data = data.sort_values(by = '关联度系数', ascending=False)
    data.to_csv('rel2.csv', index = False, encoding = 'utf-8')
    relatives_list = relatives(list_name, data, 5)
    utils.save_pickle('relatives_list.txt', relatives_list)