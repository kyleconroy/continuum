import os
import requests
import time
import json
import pprint

url = "https://api.github.com/repos/kyleconroy/continuum"

headers = {
    "Content-Type": "application/json",
    "Authorization": "token " + os.environ.get("GITHUB_TOKEN"),
}

client = requests.session(headers=headers)

timeblock = {"timestamp": time.time()}

resp = client.post(url + "/git/blobs", data=json.dumps({
    'content': json.dumps(timeblock),
    'encoding': "utf-8",
    }))

resp.raise_for_status()

blob = resp.json
pprint.pprint(blob)

resp = client.get(url + "/git/refs/heads/master")
resp.raise_for_status()

master = resp.json
pprint.pprint(master)

resp = client.get(url + "/git/commits/" + master['object']['sha'])
resp.raise_for_status()

base_commit = resp.json
pprint.pprint(master)


resp = client.post(url + "/git/trees", data=json.dumps({
    'base_tree': base_commit['tree']['sha'],
    'tree': [
        {
            'path': 'static/timestamp.json',
            'mode': '100644',
            'type': 'blob',
            'sha': blob['sha'],
        }
        ]
    }))

resp.raise_for_status()

tree = resp.json
pprint.pprint(tree)

resp = client.post(url + "/git/commits", data=json.dumps({
    'message': "Update timestamp",
    'tree': tree['sha'],
    'author': {
        'name': "Continuum Bot",
        'email': "continuum@example.com",
    },
    'parents': [ master['object']['sha'] ],
    }))

resp.raise_for_status()

commit = resp.json
pprint.pprint(commit)

resp = client.patch(url + "/git/refs/heads/master", data=json.dumps({
    'sha': commit['sha'],
    }))

resp.raise_for_status()
pprint.pprint(resp.json)
