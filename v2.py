import requests
import time

class BadgeCounter:
    def __init__(self):
        self.burl = "https://badges.roblox.com/v1/users/{}/badges"
        self.uurl = "https://users.roblox.com/v1/usernames/users"
        self.lim = 100
        self.delay = 0.5

    def getuid(self, uname):
        data = {"usernames": [uname]}
        r = requests.post(self.uurl, json=data)
        if r.status_code == 200:
            res = r.json()
            if res["data"]:
                return res["data"][0]["id"]
        return None

    def getbadges(self, uid):
        total = 0
        cursor = ""
        while True:
            url = f"{self.burl.format(uid)}?limit={self.lim}&cursor={cursor}"
            r = requests.get(url)
            if r.status_code != 200:
                break
            data = r.json()
            total += len(data["data"])
            if data["nextPageCursor"] is None:
                break
            cursor = data["nextPageCursor"]
            time.sleep(self.delay)
        return total

    def countbadges(self, uname):
        uid = self.getuid(uname)
        if not uid:
            return f"User {uname} not found"
        count = self.getbadges(uid)
        return f"User {uname} (ID: {uid}) has {count} badges"

if __name__ == "__main__":
    counter = BadgeCounter()
    uname = input("Enter Roblox username: ")
    print(counter.countbadges(uname))
