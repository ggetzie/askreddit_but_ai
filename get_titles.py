import os
import requests
import time

headers = {"User-agent": "AskReddit GPT Bot"}
params = {"t": "all"}


if __name__ == "__main__":
     titles = set()
     pcount = 0
     last_total = 0
     times = ("hour", "day", "week", "month", "year", "all")
     sorts = ("top", "hot", "new", "rising", "controversial")
     for sort_ in sorts:
          url = f"https://www.reddit.com/r/AskReddit/{sort_}/.json"
          for time_ in times:
               params["t"] = time_
               if "count" in params: 
                    del params["count"]
                    pcount = 0
               for i in range(30):
                    if len(titles) > 10000: break
                    r = requests.get(url, headers=headers, params=params)
                    print(f"Getting {r.url}")
                    if not r.status_code == 200:
                         print(f"Error: {r.text}")
                         break
                    d = r.json()
                    for item in d["data"]["children"]:
                         titles.add(item["data"]["title"])
                    params["after"] = d["data"]["after"]
                    pcount += len(d["data"]["children"])
                    params["count"] = pcount
                    with open("titles.txt", "w") as outfile:
                         outfile.write("\n".join(titles))
                    print(f"{len(titles)} titles collected so far")
                    last_total = len(titles)
                    time.sleep(2)