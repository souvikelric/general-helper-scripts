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
    repos = []
    page = 1
    today_repos = []

    while True:
        response = requests.get(
            f"{API_BASE}/user/repos",
            headers=headers,
            params={"per_page": 100, "page": page,"sort":"updated"},
        )
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1
    today = datetime.today().strftime("%Y-%m-%d")
    for repo in repos:
        if repo["updated_at"].split("T")[0] != today:
            continue
        print(repo["name"] + " | " + repo["updated_at"].split("T")[0])
        today_repos.append(repo["name"])

    print("Number of repos:", len(repos))
    return today_repos

def get_repo_commit(repo_name):
    url = f"{API_BASE}/repos/{GITHUB_USERNAME}/{repo_name}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    commits = response.json()
    return commits


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
    print(get_all_repos())


