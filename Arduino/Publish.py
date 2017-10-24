import requests
import json
import sys
headers = {'Content-Type': 'application/json'}
data = json.dumps({"topic": "com.myapp.topic1", "args": [sys.argv[1]]})
requests.post('http://127.0.0.1:8008/publish', headers=headers, data=data)
