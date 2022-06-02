import random

import requests
import httpx
import colorama
import threading
from colorama import init

tokensList = [x.strip() for x in open('tokens.txt', 'r+', encoding="utf8").readlines()]

# Token Cleaner V0.1 by xth24

init(convert=True)

_tokensList = iter(tokensList)

def getCookies():
    headers = {
        'Host': "discord.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "document",
        'DNT': "1",
        'Upgrade-Insecure-Requests': "1",
        'Connection': "keep-alive",
        'Sec-Fetch-Dest': "document",
        'Sec-Fetch-Mode': "navigate",
        'Sec-Fetch-Site': "none",
        'Sec-Fetch-User': "?1"
    }

    response = httpx.get("https://discord.com", headers=headers)
    dcf = response.headers.get('set-cookie').split('__dcfduid=')[1].split(';')[0]
    sdc = response.headers.get('set-cookie').split('__sdcfduid=')[1].split(';')[0]
    content = response.text
    requestId = content.split("r:'")[1].split("',m")[0]
    mData = content.split("m:'")[1].split("',s:")[0]

    headers = {
        'Host': "discord.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "document",
        'Content-Type': "application/json",
        'Origin': "https://discord.com",
        'DNT': "1",
        'Connection': "keep-alive",
        'Referer': "https://discord.com/",
        'Cookie': f"__dcfduid={dcf}; __sdcfduid={sdc}; locale=en-US",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'TE': "trailers"
    }
    payload = {
        "fp": {
            "e": {
                "ar": [1400, 2560],
                "cd": 24,
                "ch": False,
                "pr": 1,
                "r": [2560, 1440],
                "wb": False,
                "wd": False,
                "wn": False,
                "wp": False,
                "ws": False
            },
            "id": 3
        },
        "m": mData,
        "results": [
            "954421bd9413bc4fe101bebd63d53c79",
            "b6b93b4a643e4afcc6f3c262c1e0dfa4"
        ],
        "timing": 52
    }
    response = httpx.post(f"https://discord.com/cdn-cgi/bm/cv/result?req_id={requestId}", headers=headers, json=payload)
    cfbm = response.headers.get('set-cookie').split('__cf_bm=')[1].split(';')[0]
    return {"cfbm": cfbm, "dcf": dcf, "sdc": sdc}

def leaveServers(token, cookies):
    headers = {
        'Host': "discord.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "document",
        'Content-Type': "application/json",
        'Authorization': token,
        'X-Super-Properties': "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI4MzIzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        'X-Discord-Locale': "en-US",
        'X-Debug-Options': "bugReporterEnabled",
        'Origin': "https://discord.com",
        'DNT': "1",
        'Connection': "keep-alive",
        'Referer': "https://discord.com/channels/322850917248663552/754536220826009670",
        'Cookie': f"__dcfduid={cookies['dcf']}; __sdcfduid={cookies['sdc']}; locale=en-US; __cf_bm={cookies['cfbm']}",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'TE': "trailers"
    }
    r = httpx.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": token})
    if not r.json():
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}[/] Nothing to do!{colorama.Fore.RESET}")
        return
    for s in r.json():
        r = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{s['id']}", headers=headers, json={"lurking": False})
        if r.status_code == 204:
            print(f"{colorama.Fore.LIGHTGREEN_EX}[+] Left a server @ {s['id']}{colorama.Fore.RESET}")
        else:
            print(f"{colorama.Fore.LIGHTRED_EX}[+] Failed to leave a server @ {s['id']}{colorama.Fore.RESET}")

def clearDms(token, cookies):
    headers = {
        'Host': "discord.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.5",
        'Accept-Encoding': "document",
        'Content-Type': "application/json",
        'Authorization': token,
        'X-Super-Properties': "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAwLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTI4MzIzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        'X-Discord-Locale': "en-US",
        'X-Debug-Options': "bugReporterEnabled",
        'Origin': "https://discord.com",
        'DNT': "1",
        'Connection': "keep-alive",
        'Referer': "https://discord.com/channels/322850917248663552/754536220826009670",
        'Cookie': f"__dcfduid={cookies['dcf']}; __sdcfduid={cookies['sdc']}; locale=en-US; __cf_bm={cookies['cfbm']}",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'TE': "trailers"
    }
    r = httpx.get("https://discord.com/api/v9/users/@me/channels", headers={"Authorization": token})
    if not r.json():
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}[/] Nothing to do!{colorama.Fore.RESET}")
        return
    for u in r.json():
        r = requests.delete(f"https://discord.com/api/v9/channels/{u['id']}", headers=headers)
        if r.status_code == 200:
            print(f"{colorama.Fore.LIGHTGREEN_EX}[+] Closed a channel @ {u['id']}{colorama.Fore.RESET}")
        else:
            print(f"{colorama.Fore.LIGHTRED_EX}[+] Failed to close a channel @ {u['id']}{colorama.Fore.RESET}")

def worker():
    print(f"{colorama.Fore.LIGHTYELLOW_EX}[*] Started a thread{colorama.Fore.RESET}")
    token = next(_tokensList)
    clearDms(token, getCookies())
    leaveServers(token, getCookies())
    with open("freshtokens.txt", "a+") as f:
        f.write(token + "\n")

if __name__ == '__main__':
    try:
        print(f"{colorama.Fore.LIGHTYELLOW_EX}[!] Loaded {len(tokensList)} tokens{colorama.Fore.RESET}")
        threads = []
        for i in range(len(tokensList)):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        print(f"{colorama.Fore.LIGHTGREEN_EX}[+] Finished{colorama.Fore.RESET}")
    except Exception as e:
        print(e)