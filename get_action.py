import time
import datetime as dt
from datetime import timedelta
import pandas as pd
import pickle
import os
import math
import numpy as np
import matplotlib.pyplot as plt

action_1_path = "./data/JData_Action_201602.csv"
action_2_path = "./data/JData_Action_201603.csv"
action_3_path = "./data/JData_Action_201604.csv"

start_date = '2016-03-01'
end_date = '2016-03-31'

def get_actions():
    """

    :param start_date:
    :param end_date:
    :return: actions: pd.Dataframe
    """
    dump_path = './data/all_action.csv' 
    if os.path.exists(dump_path):
        actions = pd.read_csv(dump_path)
    else:
        action_1 = pd.read_csv(action_1_path)
        action_2 = pd.read_csv(action_2_path)
        action_3 = pd.read_csv(action_3_path)
        actions = pd.concat([action_1, action_2, action_3]) # type: pd.DataFrame
        #actions = actions[(actions.time >= start_date) & (actions.time < end_date)]
        actions.to_csv(dump_path, encoding='utf-8',index=None)
    return actions

def draw(actions):
    action_mar=actions[(actions.time >= start_date) & (actions.time < end_date)]
    action_mar['time'] = action_mar['time'].apply(lambda x: dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S").date())
    action_mar=action_mar.groupby('user_id','sku_id').sum().set_index('time')
    plt.plot(action_mar)
    plt.savefig('./action_mar.png')


if __name__ == "__main__":
    actions = get_actions()
    draw(actions)