import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

def post_creator(wpBaseURL, postStatus, wpUser, wpPass):
 
    WP_url = wpBaseURL + "/wp-json/wp/v2/posts"

    auth = HTTPBasicAuth(wpUser, wpPass)

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    current_datetime = now = datetime.now()
    payload = json.dumps({ 
        "status":postStatus,
        "title": current_datetime,
        "content": current_datetime
    })

    response = requests.request(
    "POST",
    WP_url,
    data=payload,
    headers=headers,
    auth=auth
    )

    print(response)

post_creator("https://wordpress.example.com", "publish", "superUser","adminPassword")