from instagrapi import Client
import json
import pandas as pd
import numpy as np
import time
import datetime

cl = Client()

cl.load_settings("sensitive/session.json")

df_global = pd.DataFrame()

def get_user_medias(username):
    #get user infos for one account --> Get user infos for multiple accounts
    user = cl.user_info_by_username_v1(username)

    #get user medias
    medias = cl.user_medias(user.pk, amount=0)

    #for m in medias: 
        #print(m.code, m.like_count, m.comment_count)

    #store the posts data into a database

    #as json
    with open("medias.json","w") as f: 
        for m in medias:
            f.write(json.dumps(m.model_dump(mode="json"),ensure_ascii=False) + "\n")

    df = pd.read_json("/home/simon/repos/projects/portfolio/perf_analyzer/medias.json",lines=True)

    df_user = df[["user","pk","taken_at","media_type","crosspost","coauthor_producers","sponsor_tags","location","is_paid_partnership","is_affiliate","caption_text","like_count","comment_count","play_count"]].copy()

    expanded_column = pd.json_normalize(df["user"])

    expanded_column = expanded_column.rename(columns={"pk":"pk_account"})

    df_expanded = pd.concat([expanded_column,df_user],axis=1)

    df_clean = df_expanded[['pk_account','username','is_verified','pk', 'taken_at', 'media_type', 'crosspost','coauthor_producers','sponsor_tags','location',
        'is_paid_partnership', 'is_affiliate', 'caption_text', 'like_count', 'comment_count',
        'play_count']].copy()

    scraping_datetime = datetime.datetime.now()

    df_clean["scraping_time"]=scraping_datetime

    return df_clean


users = ["french.mush","french.mush.it"]

for user in users : 
    time.sleep(2) #for instagram bot detection
    df_iteration = get_user_medias(user)
    df_global = pd.concat([df_global,df_iteration])

df_global.to_csv("test.csv")




#daily updates of the database




