import os
import json
import requests
import platform

url = "https://slack.com/api/chat.postMessage"
update_url = "https://slack.com/api/chat.update"

config_file = ".config"
task_file = ".tasks"
message_history_file = ".message"
token = None
tasks = {"tasks": []}

incompleteIcon = "https://github.com/amit08255/slack-tasklist/raw/master/assets/checked0.png"
completeIcon = "https://github.com/amit08255/slack-tasklist/raw/master/assets/checked.png"


def clearScreen():

    if platform.system() == 'Linux':
        os.system("clear")
    else:
        os.system("cls")


def saveMessageHistory(response):
    fout = open(message_history_file, "w")
    fout.write(response)
    fout.close()

def upload2Slack(channel, message, taskList):

    global token
    global url

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    payload = {"channel":channel,"as_user":True,"blocks":[{"type":"section","text":{"type":"plain_text","emoji":True,"text":message}},{"type":"divider"}]}

    for i in range(0, len(taskList), 1):

        icon = incompleteIcon

        if taskList[i]["complete"] == True:
            icon = completeIcon

        payload["blocks"].append({"type":"context","elements":[{"type":"image","image_url":icon,"alt_text":"task icon"},{"type":"mrkdwn","text":"*"+taskList[i]["title"]+"*"}]})

    payload["blocks"].append({"type":"divider"})

    payload["blocks"].append({"type":"context","elements":[{"type":"mrkdwn","text":":pushpin: The task list is sorted according to priority."}]})

    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

    saveMessageHistory(response.text)



def loadLastMessageInfo():

    if os.path.exists(message_history_file) != True:
        return None

    fin = open(message_history_file, "r")
    data = fin.read()
    fin.close()

    try:
        return json.loads(data)
    except:
        return None


def updateSlackLastMessage(message, taskList):

    global token
    global url

    history = loadLastMessageInfo()

    if history == None:
        print("\n\nFailed to retrive message history")
        return None

    if history["ok"] != True:
        print("\n\nNo successful message history found")
        return None

    channel = history["channel"]
    ts = history["ts"]

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}

    payload = {"channel":channel, "ts": ts, "as_user":True,"blocks":[{"type":"section","text":{"type":"plain_text","emoji":True,"text":message}},{"type":"divider"}]}

    for i in range(0, len(taskList), 1):

        icon = incompleteIcon

        if taskList[i]["complete"] == True:
            icon = completeIcon

        payload["blocks"].append({"type":"context","elements":[{"type":"image","image_url":icon,"alt_text":"task icon"},{"type":"mrkdwn","text":"*"+taskList[i]["title"]+"*"}]})

    payload["blocks"].append({"type":"divider"})

    payload["blocks"].append({"type":"context","elements":[{"type":"mrkdwn","text":":pushpin: The task list is sorted according to priority."}]})


    response = requests.request("POST", update_url, headers=headers, data = json.dumps(payload))

    saveMessageHistory(response.text)


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
5. Clear completed tasks
6. Update last message
7. Delete a task
0. Exit
'''

option = ""

clearScreen()
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

        saveTaskList()

    if option == "3":

        channel = input("\n\nEnter channel name: ")
        channel = channel.strip()

        message = input("\n\nEnter message: ")
        message = message.strip()

        upload2Slack(channel, message, tasks["tasks"])  

        input("\n\nPress enter to continue...")      

    if option == "4":

        print("\n\n")

        for i in range(0, len(tasks["tasks"]), 1):

            print(tasks["tasks"][i]["title"])
            print("Completed: ", tasks["tasks"][i]["complete"], "\n")

        input("\n\nPress enter to continue...")

    if option == "5":

        i = 0

        while i < len(tasks["tasks"]):

            if tasks["tasks"][i]["complete"] == True:
                del tasks["tasks"][i]
            else:
                i = i+1

        saveTaskList()

    if option == "6":

        message = input("\n\nEnter message: ")
        message = message.strip()

        updateSlackLastMessage(message, tasks["tasks"])   

        input("\n\nPress enter to continue...")

    if option == "7":

        for i in range(0, len(tasks["tasks"]), 1):
            print("\n"+str(i)+".", tasks["tasks"][i]["title"])

        index = input("\n\nEnter task index: ")
        index = int(index.strip())

        del tasks["tasks"][index]

        saveTaskList()

    clearScreen()
    print(menu)