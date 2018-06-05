# -*- coding: utf-8 -*-

import utils
import pandas as pd
import itertools


#[[a,b], [a,c], [a,d]]变为[b, c, d]
def duplicate_removal(relatives_list):
    result = []
    for item in relatives_list:
        new2 = []
        for n in item:
            for q in n:
                new2.append(q)
        guodu = list(set(new2))
        guodu.sort(key = new2.index)
        if guodu != []:
            guodu.remove(list_name[relatives_list.index(item)])
        result.append(guodu)
    return result

#两两强相关的组合，这里作为判别其他组合的基础，即是strong_related（判别强相关）的基础
def cluster_2_members(qyt):
    cluster_list = []
    for i in range(len(qyt)):
        guodu = []
        for item in qyt[i]:
            if list_name[i] in qyt[list_name.index(item)]:
                guodu.append([item])
            else:
                guodu.append('')
        cluster_list.append([x for x in guodu if x != ''])
    return cluster_list

def strong_related(index_1, index_2):
    if  [list_name[index_1]] in cluster_2[index_2]:
        return True
    else:
        return False

#聚类的基本体，cluster_num代表聚类的类别数
def cluster(cluster, cluster_num):
    cluster_list2 = []
    for i in range(len(cluster)):
        comb = list(itertools.combinations(range(len(cluster[i])), cluster_num-1))
        cluster_list1 = []
        for n in comb:
            guodu = []
            guodu2 = []
            for item in n:
                index = list_name.index(cluster[i][item][0])
                guodu2.append(index)
            a = list(itertools.combinations(guodu2, 2))
            for item1 in n:
                flag = 1
                for per in a:
                    if strong_related(per[0], per[1]) == False:
                        flag = 0
                if flag == 1:
                    guodu.append(cluster[i][item1][0])
                else:
                    guodu.append('')
            cluster_list1.append([x for x in guodu if x != ''])
        cluster_list2.append([x for x in cluster_list1 if x != []])
    return cluster_list2

def cluster_main(input_cluster):
    flag = True
    cluster_num = 3
    while flag:
        cluster_ = cluster(input_cluster, cluster_num)
        for i in cluster_:
            if i != []:
                cluster_num += 1
                break
            else:
                flag = False
    return cluster(input_cluster, cluster_num-1)
        

if __name__ == "__main__":
    relatives_list = utils.load_pickle('relatives_list.txt')
    list_name = utils.load_pickle('list_name.txt')
    list_qyt = duplicate_removal(relatives_list)
    cluster_2 = cluster_2_members(list_qyt)
    cluster_4 = cluster_main(cluster_2)
    
    column_1 = pd.Series(list_name, name='药物')  
    column_2 = pd.Series(cluster_4, name='cluster')  
    data = pd.concat([column_1, column_2], axis=1)  
    data.to_csv('cluster2.csv', index = False, encoding = 'utf-8')

        












    