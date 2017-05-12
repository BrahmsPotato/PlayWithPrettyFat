START_DATE = dt.datetime.strptime('2016-2-20', "%Y-%m-%d")#��ǰʱ��
END_DATE = dt.datetime.strptime('2016-4-10', "%Y-%m-%d")#��ǰʱ��

action_1_path = "./data/JData_Action_201602.csv"
action_2_path = "./data/JData_Action_201603.csv"
action_3_path = "./data/JData_Action_201604.csv"
comment_path = "./data/JData_Comment.csv"
product_path = "./data/JData_Product.csv"
user_path = "./data/JData_User.csv"

import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
import os
import math
import numpy as np


def add_type_count(grouped):
    #����������ȡ
    type_cnt = Counter(grouped['type'])#Ҳ������value_counts()�����Ƿ��ص���һ��Series��������������type�������
    grouped['browse_num'] = type_cnt[1]
    grouped['addcart_num'] = type_cnt[2]
    grouped['delcart_num'] = type_cnt[3]
    grouped['buy_num'] = type_cnt[4]
    grouped['favor_num'] = type_cnt[5]
    grouped['click_num'] = type_cnt[6]
    #����ת����
    grouped['delcart_addcart_ratio'] = (np.log(1 + grouped['delcart_num']) - np.log(1 + grouped['addcart_num'])).map(lambda x: '%.2f' % x)
    grouped['buy_addcart_ratio'] = (np.log(1 + grouped['buy_num']) - np.log(1 + grouped['addcart_num'])).map(lambda x: '%.2f' % x)
    grouped['buy_browse_ratio'] = (np.log(1 + grouped['buy_num']) - np.log(1 + grouped['browse_num'])).map(lambda x: '%.2f' % x)
    grouped['buy_click_ratio'] = (np.log(1 + grouped['buy_num']) - np.log(1 + grouped['click_num'])).map(lambda x: '%.2f' % x)
    grouped['buy_favor_ratio'] = (np.log(1 + grouped['buy_num']) - np.log(1 + grouped['favor_num'])).map(lambda x: '%.2f' % x)
    '''
    grouped['delcart_addcart_ratio'] = (grouped['delcart_num'] / grouped['addcart_num']) if(grouped['delcart_num'] / grouped['addcart_num'] < 1.) else 1.
    grouped['buy_addcart_ratio'] = (grouped['buy_num'] / grouped['addcart_num']) if (grouped['buy_num'] / grouped['addcart_num'] < 1.).all() else 1.
    grouped['buy_browse_ratio'] = (grouped['buy_num'] / grouped['browse_num']) if (grouped['buy_num'] / grouped['browse_num'] < 1.).all() else 1.
    grouped['buy_click_ratio'] = (grouped['buy_num'] / grouped['click_num']) if (grouped['buy_num'] / grouped['click_num'] < 1.).all() else 1.
    grouped['buy_favor_ratio'] = (grouped['buy_num'] / grouped['favor_num']) if (grouped['buy_num'] / grouped['favor_num'] < 1.).all() else 1.
    '''
    #�����ǻ�Ծ������
    timeused = (END_DATE - grouped['time']).map(lambda x: x.days)
    for i in {0, 1, 3, 7, 14, 20}:
        us = grouped[timeused <= i]
        type_cnt = Counter(us['type'])
        grouped['weight_%sday' % i] = 0.015 * type_cnt[1] + 0.6 * type_cnt[2] + 0.3 * type_cnt[4] + \
            1.0 * type_cnt[4] + 0.2*type_cnt[5] + 0.01 * type_cnt[6]
    del grouped['time']
    del grouped['type']
    return grouped
'''
    ��������ؼ��ĵط������õĻ��У�
    1���û���������������ղء��ӹ��ﳵ������ʱ��(���)(��ʱ����)
    2���û�������ղء��ӹ��ﳵ��������(���)
    3���û�ת���ʼ��û��������ֱ�����û�������ղء��ӹ��ﳵ��������Ϊ������ɣ�
    4��ƽ���ӹ��ﳵ���ղء������������������ʱ���
    5���û����3�졢7�졢10��������������ղء��ӹ��ﳵ�������Ȩֵ(���)
    6��ɾ�����ﳵ�ӹ��ﳵ�ıȣ���ɣ�
'''


def merge_action_data():  #�ϲ��û�����,�����Ӽ���ȫ����Ҫ��ȡ
    user = pd.read_csv(TRAIN_FILE)  #��ȡѵ������������
    user['time'] = pd.to_datetime(user['time'])
    user = user[(user['time'] >= START_DATE) & (user['time'] <= END_DATE)]
    grouped = user[['user_id', 'type', 'time']].groupby('user_id').apply(add_type_count)#����������ȡ
    grouped = grouped.drop_duplicates('user_id')
    return grouped


def tranform_user_age(df):
    if df == u"15������":
        df = 0
    elif df == u"16-25��":
        df = 1
    elif df == u"26-35��":
        df = 2
    elif df == u"36-45��":
        df = 3
    elif df == u"46-55��":
        df = 4
    elif df == u"56������":
        df = 5
    else:
        df = -1
    return df


def tranform_user_regtime(df):
    if (df >= 0) & (df < 10):
        df = 0
    elif (df >= 10) & (df < 30):
        df = 1
    elif (df >= 30) & (df < 60):
        df = 2
    elif (df >= 60) & (df < 120):
        df = 3
    elif (df >= 120) & (df < 360):
        df = 4
    elif (df >= 360):
        df = 5
    else:
        df = -1
    return df



#��nan����Ԥ����
def process_user_feat(user_base):
    #����ע��ʱ��
    user_base['user_reg_tm'] = user_base['user_reg_tm'].map(tranform_user_regtime)
    reg_time = pd.get_dummies(user_base['user_reg_tm'], prefix="reg_time")
    del user_base['user_reg_tm']
    #��������
    user_base['age'] = user_base['age'].map(tranform_user_age)
    age_df = pd.get_dummies(user_base['age'], prefix='age')
    del user_base['age']
    #�����Ա�
    user_base['sex'] = user_base['sex'].fillna(2)#2��ʾ����
    sex_df = pd.get_dummies(user_base['sex'], prefix='sex')
    del user_base['sex']
    #�����û��ȼ�
    user_base['user_lv_cd'] = user_base['user_lv_cd'].fillna(-1)#-1��ʾδ֪
    user_lv_df = pd.get_dummies(user_base['user_lv_cd'], prefix='user_lv_cd')
    del user_base['user_lv_cd']
    user = pd.concat([age_df, sex_df, user_lv_df, reg_time], axis=1)
    user_base = pd.concat([user_base, user], axis=1)
    return user_base


if __name__ == "__main__":
    user_base = pd.read_csv(user_path, encoding='gbk')#��ȡ�û�
    user_base['user_reg_tm'] = pd.to_datetime(user_base['user_reg_tm'])
    user_base = user_base[user_base['user_reg_tm'] <= END_DATE]
    user_base['user_reg_tm'] = (END_DATE - user_base['user_reg_tm']).map(lambda x: x.days)#ת��Ϊע������
    
    user_behavior = merge_action_data()#��ȡ�û���Ϊ����
    user_behavior = pd.merge(user_behavior, user_base, on=['user_id'], how='left')#����ͻ���NANֵ����
    user_behavior = process_user_feat(user_behavior)#��������
    user_behavior.to_csv('./feature/user_feature%s_%s.csv' % (START_DATE, END_DATE), index=None)