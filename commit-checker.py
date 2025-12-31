# a simple python script that shows total number of commits in your own github account
import requests
url = "https://api.github.com/users/souvikelric/repos"

response = requests.get(url)
data = response.json()
private_repos = 0
for val in data:
    print(val["private"])
    if val["private"]:
        private_repos += 1

print("\033[33mNumber of repositories : " + str(len(data)) + "\033[0m")
print("\033[33mNumber of private repositories : " + str(private_repos) + "\033[0m")

print(data[0]["private"])
comm_url = data[0]["commits_url"]
