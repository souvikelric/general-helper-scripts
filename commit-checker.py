# a simple python script that shows total number of commits in your own github account
import requests
from datetime import datetime, timezone
import os

GITHUB_USERNAME = "souvikelric"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
API_BASE = "https://api.github.com"



headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

today = datetime.now(timezone.utc).date()

def get_all_repos():
    repo_url = f"{API_BASE}/user/repos"
    response = requests.get(repo_url, headers=headers,params={"per_page": 100})
    response.raise_for_status()
    data = response.json()
    for d in data:
        print(d["name"])
    print("Number of repos : " + str(len(data)))

def get_today_commits():
    url = f"{API_BASE}/search/commits"
    query = f"author:{GITHUB_USERNAME} committer-date:{today}"

    params = {
        "q": query,
        "sort": "committer-date",
        "order": "desc",
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    commits = response.json().get("items", [])

    for commit in commits:
        repo = commit["repository"]["full_name"]
        message = commit["commit"]["message"].split("\n")[0]
        date = commit["commit"]["committer"]["date"].split("T")[1].split(".")[0]

        print(f"- [{repo}] | {message} ({date})")

    print(f"\nTotal commits today: {len(commits)}")


if __name__ == "__main__":
    #get_today_commits()
    get_all_repos()

