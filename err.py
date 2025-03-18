#! /usr/bin/python3
import  requests

url = "http://127.0.0.1:8000/api/auth/login/"
data = {"username": "mobius", "password": "if(Django1)open"}
headers = {}

def query(url, data=None, headers=None, post=True, token=None):
    if post:
        if token:
            headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
        res = requests.post(url, json=data, headers=headers)
        #print("Rq: " + str(res.request) + "\n")
    else:
        res = requests.get(url, data=data)
    print(str(res.status_code) + "\n")
    print(res.text+"\n")
    try:
        if not token:
            token = dict(res.json())["token"]
        else:
            # print(res.text)
            return res
    except Exception as e:
        token = "None"
        #print(str(e) + "\n" + "no token \n")
    #print(token + "\n")
    return token

token = query(url, data)

url1 = "http://127.0.0.1:8000/api/posts/"
data1 = {"title": "New post", "content": "Detials"}

query(url1, data1, post=False)
query(url1, data1, token=token)
