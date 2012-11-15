import os
import requests
import datetime

url = "https://api.github.com/kyleconroy/continuum"


client = requests.session(auth=("", os.environ.get("GITHUB_TOKEN")),
                          headers={"Content-Type": "application/json"})

timeblock = {"timestamp": time.time()}

resp = client.post(url + "/git/blobs", data=json.dumps({
    'content': json.dumps(timeblock),
    'encoding': "utf-8",
    }))

resp.raise_for_status()

blob = resp.json

resp = client.post(url + "/git/trees", data=json.dumps({
    'tree': [
        {
            'path': 'static/timestamp.json',
            'mode': '100644',
            'type': 'blob'
            'sha': blob['sha'],
        }
        ]
    }))

resp.raise_for_status()

tree = resp.json

resp = client.post(url + "/git/commits", data=json.dumps({
    'message': "Update timestamp",
    'sha': tree['sha'],
    }))

resp.raise_for_status()

commit = resp.json

print commit
