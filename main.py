import requests
import time

def getBadgeCount(userId):
    url = f"https://badges.roblox.com/v1/users/{userId}/badges"
    params = {"limit": 100, "sortOrder": "Asc"}
    headers = {"Accept": "application/json"}
    
    totalBadges = 0
    cursor = ""
    
    while True:
        if cursor:
            params["cursor"] = cursor
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            totalBadges += len(data["data"])
            
            if data["nextPageCursor"]:
                cursor = data["nextPageCursor"]
                time.sleep(0.5)
            else:
                break
        else:
            print(f"Error: Unable to fetch badge data. Status code: {response.status_code}")
            return None
    
    return totalBadges

def main():
    print("Roblox Badge Counter")
    
    while True:
        userId = input("Enter the Roblox user ID (or 'q' to quit): ")
        
        if userId.lower() == 'q':
            break
        
        try:
            userId = int(userId)
        except ValueError:
            print("Invalid user ID. Please enter a valid number.")
            continue
        
        print("Fetching badge count...")
        badgeCount = getBadgeCount(userId)
        
        if badgeCount is not None:
            print(f"The user with ID {userId} has {badgeCount} badges.")
        
        print()

if __name__ == "__main__":
    main()
