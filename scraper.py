from instagrapi import Client
import json
import pandas as pd
import numpy as np
import time
import datetime

cl = Client()

cl.load_settings("sensitive/session.json")

df_global_posts = pd.DataFrame()

def get_user_medias(username,comments_amount):
    #get user infos for one account --> Get user infos for multiple accounts
    user = cl.user_info_by_username_v1(username)

    #get user medias
    medias = cl.user_medias(user.pk, amount=3)
    rows = [m.model_dump(mode="json") for m in medias]

    #put thee medias in a dataframe
    df = pd.DataFrame(rows)

    #set up the columns in the file
    cols = ["user","pk","taken_at","media_type","crosspost","coauthor_producers","sponsor_tags","location","is_paid_partnership","is_affiliate","caption_text","like_count","comment_count","play_count"]
    df_user = df[cols].copy()
    df_user["pk"] = df["pk"].astype(str)

    #get user comments 
    df_user["comments"] = [
        [c.model_dump(mode="json") for c in cl.media_comments(pk, amount=comments_amount)]
        for pk in df_user["pk"]
    ]
    #unnest the user infos
    expanded_column = pd.json_normalize(df["user"])
    expanded_column = expanded_column.rename(columns={"pk":"pk_account"})
    df_expanded = pd.concat([expanded_column,df_user],axis=1)

    #get clean df
    df_clean = df_expanded[['pk_account','username','is_verified','pk', 'taken_at', 'media_type', 'crosspost','coauthor_producers','sponsor_tags','location',
        'is_paid_partnership', 'is_affiliate', 'caption_text', 'like_count', 'comment_count','comments',
        'play_count']].copy()

    #get scraping date time
    scraping_datetime = datetime.datetime.now()
    df_clean["scraping_time"]=scraping_datetime

    return df_clean


users = ["french.mush","french.mush.it"]

for user in users : 
    time.sleep(2) #for instagram bot detection
    df_iteration = get_user_medias(user,30)
    df_global_posts = pd.concat([df_global_posts,df_iteration])

df_global_posts = df_global_posts.reset_index(drop=True)

df_global_posts.to_csv("test.csv")




#daily updates of the database




