from instagrapi import Client
import json
import pandas as pd
import numpy as np
import time
import datetime

cl = Client()

cl.load_settings("sensitive/session.json")

#get user infos for one account --> Get user infos for multiple accounts
user = cl.user_info_by_username_v1("french.mush")


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


df_clean.to_csv("test.csv")




#daily updates of the database




