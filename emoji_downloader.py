#!/bin/python3
import requests, os, shutil 

if os.path.isfile("./token.txt"):
    token = open("token.txt").read().strip()
else:
    token = input("token : ")
    open("token.txt", "w").write(token)

def restrict(str_):
    if os.name == "nt":
        str_ = str_.translate({ord(i): None for i in '\/:*?"<>|'})
    else:
        str_ = str_.replace("/", "")
    if len(str_) == 0:
        str_ = "no name"
    return str_

if __name__ == "__main__":
    guilds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers={"authorization": token}).json()
    i = 0
    msg = ""
    server_ids = []
    server_names = []
    for guild in guilds:
        i += 1
        server_ids.append(guild["id"])
        server_names.append(guild["name"])
        msg += str(i) + " | " + guild["name"] + "\n"
    print(msg)
    a = input("Choose the guild : ")
    if a.isdigit():
        server_id = server_ids[int(a) + 1]
        server_name = server_names[int(a) + 1]
    else:
        print("not a num")
        exit(0)
    server_folder = restrict(server_name)
    if os.path.isdir("./" + server_folder):
        print("removing the folder " + server_folder)
        shutil.rmtree("./" + server_folder)
    os.mkdir("./" + server_folder)
    print("getting the emoji list of " + server_name)
    emojis = requests.get("https://discord.com/api/v8/guilds/" + server_id + "/emojis", headers={"authorization": token}).json()
    i = 0
    for emoji in emojis:
        i += 1
        if emoji["animated"]:
            with open("./" + server_folder + "/" + emoji["name"] + ".gif", "wb") as f:
                print("downloading " + emoji["name"] + " (animated) (" + str(i) + "/" + str(len(emojis)) + ")")
                f.write(requests.get("https://cdn.discordapp.com/emojis/" + emoji["id"] + ".gif?v=1").content)
        else:
            with open("./" + server_folder + "/" + emoji["name"] + ".png", "wb") as f:
                print("downloading " + emoji["name"] + " (" + str(i) + "/" + str(len(emojis)) + ")")
                f.write(requests.get("https://cdn.discordapp.com/emojis/" + emoji["id"] + ".png?v=1").content)
    print("finished downloading all emojis")
