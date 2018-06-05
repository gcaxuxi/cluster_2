# -*- coding: utf-8 -*-

import math
from math import log
import utils

#数据集


list_name = utils.load_pickle('list_name.txt')
list_fre = utils.load_pickle('list_fre.txt')
combinations_fre = utils.load_pickle('combinations_fre.txt')
combinations_list = utils.load_pickle('combinations_list.txt')
data = list(range(len(list_name)))

def calculate_correlation(pre, suf):
    flag_1, flag_2, flag_3 = 1, 1, 1
    if pre == suf or (pre,suf) not in combinations_list:
        result = 0
    else:
        i = combinations_list.index((pre, suf))
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
        result = (H_pre + H_suf - H_pre_suf)/((H_pre**0.5)*(H_suf**0.5))
    return result

#计算欧几里得距离,a,b分别为两个元组
def dist(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))

#dist_min
def dist_min(Ci, Cj):
    return min(calculate_correlation(i, j) for i in Ci for j in Cj)
#dist_max
def dist_max(Ci, Cj):
    return max(calculate_correlation(i, j) for i in Ci for j in Cj)
#dist_avg
def dist_avg(Ci, Cj):
    return sum(calculate_correlation(i, j) for i in Ci for j in Cj)/(len(Ci)*len(Cj))

#找到距离最小的下标
def find_Max(M):
    max = 0
    x = 0; y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i != j and M[i][j] > max:
                max = M[i][j];x = i; y = j
    return (x, y, max)

#算法模型：
def AGNES(dataset, dist, k):
    #初始化C和M
    C = [];M = []
    for i in dataset:
        Ci = []
        Ci.append(i)
        C.append(Ci)
    for i in C:
        Mi = []
        for j in C:
            Mi.append(dist(i, j))
        M.append(Mi)
    #print('1', M)
    q = len(dataset)
    #合并更新
    while q > k:
        x, y, max = find_Max(M)
        C[x].extend(C[y])
        C.remove(C[y])
        M = []
        for i in C:
            Mi = []
            for j in C:
                Mi.append(dist(i, j))
            M.append(Mi)
        q -= 1
        print(q)
    return C, M


c, m  = AGNES(data, dist_avg, 5)
cluster = []
for item in c:
    clu = []
    for i in item:
        clu.append(list_name[i])
    cluster.append(clu)  



