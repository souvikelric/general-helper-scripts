# a simple python script that shows total number of commits in your own github account


from dataclasses import dataclass
import sys
import requests
from datetime import datetime, timezone
import os

@dataclass
class bgColors():
    green = "\033[32m"
    red = "\033[31m"
    reset = "\033[0m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    cyan = "\033[96m"


def print_helper(message: str, color: str = bgColors.magenta) -> None:
    print(color + message + bgColors.reset)


#GITHUB_USERNAME = "souvikelric"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
API_BASE = "https://api.github.com"



headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

today = datetime.today().strftime("%Y-%m-%d")

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
        if response.status_code >= 400:
            print_helper("Error in getting response, check username", bgColors.red)
            exit(1)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1
    
    print_helper("Repos Contributed to today")
    for repo in repos:
        if repo["updated_at"].split("T")[0] != today:
            continue
        print_helper(repo["name"],bgColors.yellow)
        today_repos.append(repo["name"])
    print()
    return today_repos

def get_repo_commits(repo_name):
    url = f"{API_BASE}/repos/{GITHUB_USERNAME}/{repo_name}/commits"
    page_num = 1
    all_commits = []

    while True:
        response = requests.get(
            url,
            headers=headers,
            params={"per_page": 100, "page": page_num},
        )
        if response.status_code >= 400:
            print_helper("Error in getting response, check username", bgColors.red)
            exit(1)
        response.raise_for_status()

        commits = response.json()

        if not commits:  # no more pages
            break

        all_commits.extend(commits)
        page_num += 1

    return all_commits


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
    if len(sys.argv) > 1 and sys.argv[1] == "--username":
        #check if value is passed for second argument
        if len(sys.argv) > 2:
            GITHUB_USERNAME = sys.argv[2]
        else:
            print("Please pass value of username after --username")
            exit(1)
    elif len(sys.argv) > 1:
        print("Invalid argument")
        exit(1)
    else:
        GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]

    repos = get_all_repos()
    print_helper("All commits for today")
    all_repo_commits = 0
    for r in repos:
        commits = get_repo_commits(r)
        for c in commits:
            if c["commit"]["committer"]["date"].split("T")[0] != today:
                continue
            print_helper(r + " | " + c["commit"]["message"] + " | " + c["commit"]["committer"]["date"].split("T")[0],bgColors.cyan)
            all_repo_commits += 1
    print()
    print_helper(f"Total commits today: {all_repo_commits}")
    print()
    
