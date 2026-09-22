from instagrapi import Client

cl = Client()
cl.login_by_sessionid("23852741267%3AqeZwuaMe10ZxO9%3A3%3AAYmAtxc9a7RuhhrnRX-1SmxNVQnGXvTHtOs3G9873g")
cl.dump_settings("session.json")
print("session sauvegarde")
