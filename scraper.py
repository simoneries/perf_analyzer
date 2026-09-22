from instagrapi import Client
import json

cl = Client()

cl.load_settings("session.json")

user = cl.user_info_by_username("xavierkmk")

with open("instagram.json", "w") as f:
    json.dump(user.model_dump(), f, indent=2, default=str)



