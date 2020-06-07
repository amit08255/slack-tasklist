import os
import json
import requests

url = "https://slack.com/api/chat.postMessage"

config_file = ".config"
task_file = ".tasks"
token = None
tasks = {"tasks": []}

incompleteIcon = "https://as1.ftcdn.net/jpg/01/29/11/32/500_F_129113243_JHc6iRj7TmeEOaB2CK7YXFkD5PUpE4fN.jpg"
completeIcon = "https://t3.ftcdn.net/jpg/01/29/11/32/240_F_129113249_oGxjEE4PPBpt8RtUFEZNgf4soRctzq2d.jpg"

def upload2Slack(channel, message, taskList):

    global token
    global url

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    payload = {"channel":channel,"as_user":True,"blocks":[{"type":"section","text":{"type":"plain_text","emoji":True,"text":message}},{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"Today's task list:"}}]}

    for i in range(0, len(taskList), 1):

        icon = incompleteIcon

        if taskList[i]["complete"] == True:
            icon = completeIcon

        payload["blocks"].append({"type":"context","elements":[{"type":"image","image_url":icon,"alt_text":"task icon"},{"type":"mrkdwn","text":"*"+taskList[i]["title"]+"*"}]})

    payload["blocks"].append({"type":"divider"})

    payload["blocks"].append({"type":"context","elements":[{"type":"mrkdwn","text":":pushpin: The task list is sorted according to priority."}]})
            

    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    
    print(response.text.encode('utf8'))


def saveTaskList():

    global tasks

    fout = open(task_file, "w")
    fout.write(json.dumps(tasks))
    fout.close()



if os.path.exists(config_file) != True:
    fout = open(config_file, "w")
    
    token = input("Enter slack token: ")
    token = token.strip()

    fout.write(token)
    fout.close()
else:
    fin = open(config_file, "r")
    token = fin.read()
    fin.close()

if os.path.exists(task_file) == True:
    fin = open(task_file, "r")
    data = fin.read()
    tasks = json.loads(data)
    fin.close()


menu = '''
1. Add task
2. Complete task
3. Status update on slack
4. List tasks
0. Exit
'''

option = ""

print(menu)

while option != "0":

    option = input("\n\nEnter option: ")
    option = option.strip()

    if option == "1":
        
        title = input("\n\nEnter task title: ")
        title = title.strip()

        tasks["tasks"].append({"title": title, "complete": False})

        saveTaskList()

    if option == "2":

        for i in range(0, len(tasks["tasks"]), 1):
            print("\n"+str(i)+".", tasks["tasks"][i]["title"])

        index = input("\n\nEnter task index: ")
        index = int(index.strip())

        tasks["tasks"][index]["complete"] = True

    if option == "3":

        channel = input("\n\nEnter channel name: ")
        channel = channel.strip()

        message = input("\n\nEnter message: ")
        message = message.strip()

        upload2Slack(channel, message, tasks["tasks"])        

    if option == "4":

        print("\n\n")

        for i in range(0, len(tasks["tasks"]), 1):

            print(tasks["tasks"][i]["title"])
            print("Completed: ", tasks["tasks"][i]["complete"], "\n")

    print(menu)