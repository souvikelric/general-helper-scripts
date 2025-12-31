# a simple python script that shows total number of commits in your own github account
import requests
from datetime import datetime, timezone
import os

GITHUB_USERNAME = "souvikelric"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

today = datetime.now(timezone.utc).date()

def get_today_commits():
    url = "https://api.github.com/search/commits"
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
        sha = commit["sha"][:7]
        date = commit["commit"]["committer"]["date"]

        print(f"- [{repo}] {sha} | {message} ({date})")

    print(f"\nTotal commits today: {len(commits)}")


if __name__ == "__main__":
    get_today_commits()

