# a simple python script that shows total number of commits in your own github account
import requests
url = "https://api.github.com/users/souvikelric/repos"

response = requests.get(url)
data = response.json()
comm_url = data[0]["commits_url"]

comm_response = requests.get(comm_url)
comm_data = comm_response.json()
print(comm_data)