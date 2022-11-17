import requests
import getpass
import json
from requests.auth import HTTPBasicAuth

def search(headers,auth, fixversion):
    search = "https://jira.tools.us/rest/api/2/search"
    search_query = {
        'jql': 'project = project_name AND status = Closed AND fixVersion =' + str(fixversion)
    }
    response = requests.request(
    "GET",
    search,
    headers=headers,
    auth=auth,
    params=search_query
    )
    # Decode Json string to Python
    json_data = json.loads(response.text)
    list1 = list()
    # Display issues
    for item in json_data["issues"]:
        list1.append(item["id"])

    return list1
def commit(list, headers,auth):
    for i in list:

        new = "https://jira.tools.us/rest/dev-status/latest/issue/detail?issueId=" +str(i)
        arg = "&applicationType=stash&dataType=repository"
        url = new + arg
        query = {
                'jql': 'project =project_name'
            }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            params=query
        )
        json_data = json.loads(response.text)
        x = json_data["detail"]
        out = x[0]
        output = out["repositories"]

        for i in output:
            repo_name = i['name']
            commit_id = i['commits']
            for suj in commit_id:
                merge = suj['merge']
                if merge == True:

                    com = suj['id']
                    d = { repo_name : com }
                    stash(headers,auth,repo_name,com)

def stash(headers,auth,repo_name,com):
        repo = "https://stash.tools.us/projects/project_name/repos/"+str(repo_name)
        tag = "/tags?q=target+=+%22"+str(com)
        final = "%22"
        url = repo+tag+final
        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        json_data = json.loads(response.text)
        x = json_data["values"]
        for i in x:
            for key, value in i.items():
                if key == "latestCommit":
                    if value == com:
                        out = i['displayId']
                        d = { repo_name : out }
                        print(d)
                        filehandler = open("manifest.yml", "a")
                        json.dump(d, filehandler, indent = 2)

def main_function():
    username = input("Username: ")
    password = getpass.getpass('Enter your Password:')
    fixversion = input("Fix Version: ")
    auth = HTTPBasicAuth(username, password)
    headers = {
        "Accept": "application/json"
    }
    list = search(headers,auth,fixversion)
    commit(list,headers,auth)
    

if __name__ == "__init__":
    main_function()
# Main Code
if __name__ == "__main__":
    main_function()
