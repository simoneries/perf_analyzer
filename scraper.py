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
medias = cl.user_medias(user.pk, amount=3)

#for m in medias: 
    #print(m.code, m.like_count, m.comment_count)

#store the posts data into a database

#as json
with open("medias.json","w") as f: 
    for m in medias:
        f.write(json.dumps(m.model_dump(mode="json"),ensure_ascii=False) + "\n")

df = pd.read_json("/home/simon/repos/projects/portfolio/perf_analyzer/medias.json",lines=True)


#daily updates of the database




