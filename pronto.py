#Author: Paul Estrada
#Email: paul257@ohs.stanford.edu
#URL: https://github.com/Society451/Better-Pronto

import requests, logging
from datetime import datetime
from dataclasses import dataclass, asdict

API_BASE_URL = "https://stanfordohs.pronto.io/"
class BackendError(Exception):
    pass
# Dataclass for device information
@dataclass
class DeviceInfo:
    browsername: str
    browserversion: str
    osname: str
    type: str
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#AUTHENTICATION FUNCTIONS
# Function to verify user email
def requestVerificationEmail(email):
    url = "https://accounts.pronto.io/api/v1/user.verify"
    payload = {"email": email}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise BackendError(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise BackendError(f"An error occurred: {err}")

# Function to log in using email and verification code
def verification_code_to_login_token(email, verification_code):
    url = "https://accounts.pronto.io/api/v3/user.login"
    device_info = DeviceInfo(
        browsername="Firefox",
        browserversion="130.0.0",
        osname="Windows",
        type="WEB"
    )
    request_payload = {
        "email": email,
        "code": verification_code,
        "device": asdict(device_info)
    }
    headers = {
        "Content-Type": "application/json"
    }
    logger.info(f"Payload being sent: {request_payload}")
    try:
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get user accesstoken from logintoken
def login_token_to_access_token(logintoken):
    url = f"{API_BASE_URL}api/v1/user.tokenlogin"
    device_info = {
        "browsername": "firefox",
        "browserversion": "130.0.0",
        "osname": "macOS",
        "type": "WEB",
        "uuid": "314c9314-d5e5-4ae4-84e2-9f2f3938ca28",
        "osversion": "10.15.6",
        "appversion": "1.0.0",
        }
    request_payload = {
        "logintokens": [logintoken],
        "device": device_info,
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=request_payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")


#BUBBLE FUNCTIONS
# Function to get all user's bubbles
def getUsersBubbles(access_token):
    url = f"{API_BASE_URL}api/v3/bubble.list"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",  # Ensure 'Bearer' is included
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get last 50 messages in a bubble, given bubble ID 
# and an optional argument of latest message ID, which will return a list of 50 messages sent before that message
def get_bubble_messages(access_token, bubbleID, latestMessageID=None):
    url = f"{API_BASE_URL}api/v1/bubble.history"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {"bubble_id": bubbleID}
    if latestMessageID is not None:
        request_payload["latest"] = latestMessageID

    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
def send_reaction(access_token, reaction, id):

    url = f"{API_BASE_URL}api/clients/messages/{id}/reactions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "emoji": reaction,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
#Function to get information about a bubble
def get_bubble_info(access_token, bubbleID):
    url = f"{API_BASE_URL}api/v2/bubble.info"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to mark a bubble as read
def markBubble(access_token, bubbleID, message_id=None):
    url = f"{API_BASE_URL}api/v1/bubble.mark"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
        "message_id": message_id
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

def membershipUpdate(access_token, bubbleID, marked_unread=False):
    url = f"{API_BASE_URL}api/v1/membership.update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
        "marked_unread": marked_unread,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
#Function to create DM
def createDM(access_token, id, orgID):
    url = f"{API_BASE_URL}api/v1/dm.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "organization_id": orgID,
        "user_id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to create a bubble/group
def createBubble(access_token, orgID, title, category_id):
    url = f"{API_BASE_URL}api/v1/bubble.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    if category_id is not None:
        request_payload = {
        "organization_id": orgID,
        "title": title,
        "category_id": category_id,
    }
    else:
        request_payload = {
        "organization_id": orgID,
        "title": title,
    }

    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")


#Function to add a member to a bubble
#people is a list of user IDs, in the form of [5302519, 5302367]


async def addMemberToBubble(access_token, bubbleID, people):
    url = f"{API_BASE_URL}api/clients/chats/{bubbleID}/memberships/batch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "user_ids": people,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to kick user from a bubble
#users is a list of user IDs, in the form of [5302519]
async def kickUserFromBubble(access_token, bubbleID, users):
    url = f"{API_BASE_URL}api/v1/bubble.kick"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
        "users": users,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")


#Function to update a bubble
#title is the new title of the bubble, in the form of a string
#category_id is the new category ID of the bubble, in the form of an integer such as 173528
#changetitle = allow "owner" or "member" to change the title of the bubble
#addmember = allow "owner" or "member" to add a member to the bubble
#leavegroup = allow "owner" or "member" to leave the bubble
#create_message = allow "owner" or "member" to create a message in the bubble
#assign_task = allow "owner" or "member" to assign a task in the bubble
#pin_message = allow "owner" or "member" to pin a message in the bubble or "null"
#changecategory = allow "owner" or "member" to change the category of the bubble
#removemember = allow "owner" or "member" to remove a member from the bubble
#create_videosession = allow "owner" or "member" to create a video session in the bubble
#videosessionrecordcloud = allow "owner" or "member" to record a video session in the cloud
#create_announcement = allow "owner" or "member" to create an announcement in the bubble

def updateBubble(access_token, bubbleID, title=None, category_id=None, changetitle=None, addmember=None, leavegroup=None, create_message=None, assign_task=None, pin_message=None, changecategory=None, removemember=None, create_videosession=None, videosessionrecordcloud=None, create_announcement=None):
    url = f"{API_BASE_URL}api/v1/bubble.update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "bubble_id": bubbleID,
    }
    if title is not None:
        request_payload["title"] = title
    if category_id is not None:
        request_payload["category_id"] = category_id
    if changetitle is not None:
        request_payload["changetitle"] = changetitle
    if addmember is not None:
        request_payload["addmember"] = addmember
    if leavegroup is not None:
        request_payload["leavegroup"] = leavegroup
    if create_message is not None:
        request_payload["create_message"] = create_message
    if assign_task is not None:
        request_payload["assign_task"] = assign_task
    if pin_message is not None:
        request_payload["pin_message"] = pin_message
    if changecategory is not None:
        request_payload["changecategory"] = changecategory
    if removemember is not None:
        request_payload["removemember"] = removemember
    if create_videosession is not None:
        request_payload["create_videosession"] = create_videosession
    if videosessionrecordcloud is not None:
        request_payload["videosessionrecordcloud"] = videosessionrecordcloud
    if create_announcement is not None:
        request_payload["create_announcement"] = create_announcement

    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#Function to pin message to bubble
#Example {bubble_id: 3955365, pinned_message_id: 96930584, pinned_message_expires_at: "2025-01-18 23:12:18"}
# or send pinned_messageid: "null" to unpin the message
def pinMessage(access_token, pinned_message_id, pinned_message_expires_at):
    url = f"{API_BASE_URL}api/v1/bubble.update"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "pinned_message_id": pinned_message_id,
        "pinned_message_expires_at": pinned_message_expires_at,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
def getAllUsers(access_token):
    cursor = None
    isnext = True
    users = []

    """Main loop for running the bot and web server."""
    while isnext is True:
        data = getUsers(access_token, cursor)
        for user in data['data']:
            users.append(user)
        cursor = data['cursors']['next']
        if cursor is None:
            isnext = False
    return users
def getUsers(access_token, cursor):
    url = f"{API_BASE_URL}api/clients/users/search?page[size]=100&filter[relation]=all"
    if cursor is not None:
        url += f"&cursor={cursor}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "Sec-CH-UA": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "_ga=GA1.1.1368364421.1735332210; intercom-device-id-jvnadqxj=be4e47aa-1106-4e57-843e-7d0b101c99f5; _ga_KLK6801VTF=GS1.1.1741885363.3.0.1741885369.54.0.0; _ga_9NSJK923MZ=GS1.1.1741885363.3.0.1741885369.0.0.0; _gcl_au=1.1.746071284.1743442143; api_token=3tcOfZqY6B4T7MBLpuVa897Gf5MTWgCmT0JS2S4t.1371177746; pacct_2245_5301889=stanfordohs.pronto.io|Taylan|Derstadt|Stanford%20Online%20High%20School|stanfordohs|/files/orgs/2245/profilepic?pronto_time=1682388066; _ga_L1NEN7Z2H9=deleted; intercom-id-jvnadqxj=dfe3f18d-2a9d-45b2-8672-397aa4a77786; _ga_W4LTBQT59D=GS1.1.1746121632.34.0.1746121641.0.0.0; _ga_L1NEN7Z2H9=GS1.1.1746121627.7.1.1746121643.0.0.0; intercom-session-jvnadqxj=; _ga_0WN12QHPG4=GS2.1.s1746480226$o9$g0$t1746480226$j0$l0$h0; _uetsid=a81e21802b8111f0afbd65232e717d6f; _uetvid=c851e300002911f096ed1fc1154a6612; amp_e9074a=TGATbwFaNLxbsdOkEUrPty...1iqm6sjl3.1iqm6snum.h.1k.25; _ga_FK716NGXTQ=GS2.1.s1746649631$o17$g1$t1746649639$j52$l0$h0; pronto_session=eyJpdiI6IjduZ3R3WEdZSXNwRjNWeE44emJ6THc9PSIsInZhbHVlIjoiSE1ybkllRzNUSmNtRDBEZWhIMUtGdkRVVXVjN0NLK1gzMENYTjIzSGdGQnR3eFN6OVRzRFVNU2ZHUisrV2VnRnFpcGxQUzhqQ1NCWVpCZ01tSmc1QWFXSWtCTC9oampxVHRFYlhTbmQ4OURTOENac2M4dHJGMk4vTFpJa0k3enEiLCJtYWMiOiIzMTI2Zjg3ZDFmMTQ1NDljZGJmNTk4NTgzMGVjYzFhNzBhYTYzODVmZjg4Mjk3OTMxMDg5NDM5ZDg2M2U4ZjY1IiwidGFnIjoiIn0%3D",
        "Authorization": f"Bearer {access_token}",
    }


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
async def getInvites(access_token, bubbleID):
    url = f"{API_BASE_URL}api/clients/groups/{bubbleID}/invites"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.get(url, headers=headers,)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
async def deleteInvite(access_token, code):
    url = f"{API_BASE_URL}api/clients/invites/{code}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        response = requests.delete(url, headers=headers,)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
#Function to create invite link
#access is the access level of the invite, expiration is the expiration date of the invite
#access example: access: "internal"
#^this allows for only users with the link and who are a part of the org to join
#expiration example: expires: "2024-12-09T16:08:34.332Z"

def createInvite(bubbleID, access, expires, access_token):
    url = f"{API_BASE_URL}api/clients/groups/{bubbleID}/invites"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "access": access,
        "expires": expires,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")



#MESSAGE FUNCTIONS
# Function to send a message to a bubble
def send_message_to_bubble(access_token, bubbleID, created_at, message, userID, uuid, parentmessage_id):
    url = f"{API_BASE_URL}api/v1/message.create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    if (parentmessage_id == None):
        request_payload = {
        "bubble_id": bubbleID,
        "created_at": created_at,
        "id": "Null",
        "message": message,
        "messagemedia": [],
        "user_id": userID,
        "uuid": uuid  
    }
    else:
        request_payload = {
            "bubble_id": bubbleID,
            "created_at": created_at,
            "id": "Null",
            "message": message,
            "messagemedia": [],
            "parentmessage_id": parentmessage_id,
            "user_id": userID,
            "uuid": uuid  
        }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to add a reaction to a message
def addReaction(access_token, messageID, reactiontype_id):
    url = f"{API_BASE_URL}api/v1/message.addreaction"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
        "reactiontype_id": reactiontype_id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to remove a reaction from a message
def removeReaction(access_token, messageID, reactiontype_id):
    url = f"{API_BASE_URL}api/v1/message.removereaction"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
        "reactiontype_id": reactiontype_id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to edit a message
def editMessgae(access_token, newMessage, messageID):
    url = f"{API_BASE_URL}api/v1/message.edit"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message": newMessage,
        "message_id": messageID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to delete a message
def deleteMessage(access_token, messageID):
    url = f"{API_BASE_URL}api/v1/message.delete"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "message_id": messageID,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")


#USER INFO FUNCTIONS
# Function to get user information
def userInfo(access_token, id):
    url = f"{API_BASE_URL}api/v1/user.info"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to get a user's mutual groups
def mutualGroups(access_token, id):
    url = f"{API_BASE_URL}api/v1/user.mutualgroups"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "id": id,
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

# Function to set online/offline status
def setStatus(access_token, userID, isonline, lastpresencetime):
    url = f"{API_BASE_URL}api/clients/users/presence"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {  
        "data": [
            {
                "user_id": userID,
                "isonline": isonline,
                "lastpresencetime": lastpresencetime
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")
        
#OTHER Functions
# Search for message function
#EXAMPLE: {search_type: "files", size: 25, from: 0, orderby: "newest", query: "hello there", user_ids: [5302419]}
def searchMessage(access_token, query, bubbleIDs, user_ids, start_date, end_date, fromnum, orderby, size):
    url = f"{API_BASE_URL}api/v1/message.search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "search_type": "messages",
        "size": size,
        "from": fromnum,
        "query": query,
    }
    if bubbleIDs is not None:
        request_payload["bubble_ids"] = bubbleIDs
    if orderby is not None:
        request_payload["orderby"] = orderby
    if user_ids is not None:
        request_payload["user_ids"] = user_ids
    if start_date is not None:
        request_payload["start_date"] = start_date
    if end_date is not None:
        request_payload["end_date"] = end_date
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")

#{"orderby":["firstname","lastname"],"includeself":true,"bubble_id":"3640189","page":1}
def bubbleMembershipSearch(access_token, bubble_id, orderby=["firstname", "lastname"], includeself=True, page=None):
    url = f"{API_BASE_URL}/api/v1/bubble.membershipsearch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    request_payload = {
        "orderby": orderby,
        "includeself": includeself,
        "bubble_id": bubble_id,
    }
    if page is not None:
        request_payload["page"] = page
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
        if response.status_code == 401:
            raise BackendError(f"HTTP error occurred: {http_err}")
        else:
            raise BackendError(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        raise BackendError(f"Request exception occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise BackendError(f"An unexpected error occurred: {err}")