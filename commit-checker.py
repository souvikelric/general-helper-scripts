# a simple python script that shows total number of commits in your own github account
import requests
url = "https://api.github.com/users/souvikelric/repos"

response = requests.get(url)
data = response.json()
for val in data:
    print(val["name"])

comm_url = data[0]["commits_url"]
