# a simple python script that shows total number of commits in your own github account


import sys
import requests
from datetime import datetime, timezone
import os
import argparse

from utils import bgColors, print_helper

#GITHUB_USERNAME = "souvikelric"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
API_BASE = "https://api.github.com"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def get_local_midnight_utc():
    """Returns the ISO 8601 string for local midnight in UTC."""
    return datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def is_today(utc_date_str):
    """Checks if a UTC ISO date string corresponds to today in local time."""
    utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return utc_dt.astimezone().date() == datetime.now().date()

def get_all_repos():
    repos = []
    page = 1
    today_repos = []

    while True:
        response = requests.get(
            f"{API_BASE}/user/repos",
            headers=headers,
            params={"per_page": 100, "page": page,"sort":"updated","since":get_local_midnight_utc()},
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
        if not is_today(repo["updated_at"]):
            continue
        print_helper(repo["name"],bgColors.yellow)
        today_repos.append(repo["name"])
    print()
    return today_repos

def get_repo_commits(repo_name, since=None):
    url = f"{API_BASE}/repos/{GITHUB_USERNAME}/{repo_name}/commits"
    page_num = 1
    all_commits = []
    params = {"per_page": 100, "page": page_num}
    if since:
        params["since"] = since

    while True:
        params["page"] = page_num
        response = requests.get(
            url,
            headers=headers,
            params=params,
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
    today = datetime.today().strftime("%Y-%m-%d")
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
    #use argparse library instead
    #check if username is passed as argument

    parser = argparse.ArgumentParser(description="Check daily commits")
    parser.add_argument("--username", help="GitHub username to check")
    args = parser.parse_args()

    if args.username:
        GITHUB_USERNAME = args.username
    else:
        GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]

    repos = get_all_repos()
    print_helper("All commits for today")
    all_repo_commits = 0
    for r in repos:
        commits = get_repo_commits(r, since=get_local_midnight_utc())
        for c in commits:
            if not is_today(c["commit"]["committer"]["date"]):
                continue
            print_helper(r + " | " + c["commit"]["message"] + " | " + c["commit"]["committer"]["date"].split("T")[0],bgColors.cyan)
            all_repo_commits += 1
    print()
    print_helper(f"Total commits today: {all_repo_commits}")
    print()
    
