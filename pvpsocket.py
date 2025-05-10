# Standard library imports
import asyncio
import json
import logging
import mimetypes
import os
import pathlib
import random
import re
import sys
import time
import uuid
import threading
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from io import BytesIO
from dateutil.relativedelta import relativedelta
import pycurl
import emoji
global overthrowlist
# Third-party imports
import requests
import websockets
from aiohttp import web
googlelogurl = 'https://script.google.com/macros/s/AKfycbw03acp1Zv4xN59kO1Hy2Wwux0YKK0M9QQ5Nvm045brr04SVPMVyhjsc-cAmLlzNMyD/exec'
google2 = 'https://script.google.com/macros/s/AKfycbx7IiNipRuFOyCl-V8fTXXStN5JjfLhCDIZgpsYj33Mfvn4WTIs2oNeWjH4U6ujeKyJ/exec'
the_doc_id = '1aBEAsjVUiQ9An4GNYo9VCiAqAPX09RWzg4P3f0dJkFw'
femboy_ai_doc_id = '10NldJ--lM-jJJXXnmdhzLI5Jn1UNdV3k_ljptDk3bZk'
doc_id = '1jgbKbYzvqDYG2hjnkjwnj2L97hztrcUiyjkiU_FZM8I'
femboy_doc_id = '1KWbQKENSmrQu88C9XvzkxNQttQSU45NGsDijftIZ6UM'
proper_doc_id = '1COR7Vcc_mP3yIn_4uoZbJ3baA98z0utZuGbA31vpOWk'
t_or_d_doc_id = '1Ha6XJIvYxt0k3zszzb6WGeCWelfK81tImtMmKDJ-d9U'
emoji_doc_id = '1PpWaGNahz6RAB8O3f0Sx59NaoJ5ObGwKSh0yG3g030E'
recap_doc_id = '1v0TB8fpWegVwqABUTL0-pAQiM82yaMxEe2z1ue52EzI'
overthrow_doc_id = '172WAXounrWfFuFgaQzwmmPZHV5Uldt2LWwN-BX7kH7k'
bots_doc_id = '12OJ4m3zZHRu0fqE4gcfm4vToe7KvKDUIxv-boHdthH4'
full_stats_person = '1JzWFtvR6rh7u3TM8S6Qk7NMBN4xEN_-SGWqWPetEQKU'
# Local imports
from ProntoBackend.pronto import *
from ProntoBackend.readjson import *
from ProntoBackend.systemcheck import *
from ProntoBackend.accesstoken import *
from ProcessScripts.pvp import MainBot
import base64
global mewmode
#global all_users
#all_users = getAllUsers(accesstoken)
mewmode = 0
global emojimode
emojimode = 0
global superemojibanish
superemojibanish = 0
# Setup logging
accesstoken = getAccesstoken()
auth_path, chats_path, bubbles_path, loginTokenJSONPath, authTokenJSONPath, verificationCodeResponseJSONPath, settings_path, encryption_path, logs_path, settingsJSONPath, keysJSONPath, bubbleOverviewJSONPath, users_path = createappfolders()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}
# Constants
API_BASE_URL = "https://stanfordohs.pronto.io/"
USER_ID = "5301889"
INT_USER_ID = 5301889
MAIN_BUBBLE_ID = "4367071"
LOG_CHANNEL_ID = "4283367"
ORG_ID = 2245
MESSAGE_MAX_LENGTH = 750
global beta_banished
beta_banished = []
WARNING_THRESHOLD = 3
RATE_LIMIT_SECONDS = 5
FLAG_SETTING = 3
overthrow_chat_id = 4345656
eightball_responses = [
    "It is certain.", "Without a doubt.", "You may rely on it.", "Yes – definitely.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Don't count on it.", "My reply is no.", "Very doubtful.", "The cosmic muffin's will is uncertain."
]
def get_random_emoji():
    all_emojis = list(emoji.EMOJI_DATA.keys())
    return random.choice(all_emojis)
global ratelimit
ratelimit = datetime.now()
global saftymodeemoji
saftymodeemoji = 0
# Trivia URLs
TRIVIA_URLS = {
    'arts': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/arts_and_literature.json",
    'entertainment': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/entertainment.json",
    'food': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/food_and_drink.json",
    'geography': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/geography.json",
    'history': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/history.json",
    'language': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/language.json",
    'mathematics': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/mathematics.json",
    'music': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/music.json",
    'people': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/people_and_places.json",
    'religion': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/religion_and_mythology.json",
    'science': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/science_and_nature.json",
    'sport': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/sport_and_leisure.json",
    'tech': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/tech_an_video_games.json",
    'toys': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/toys_and_games.json",
    'misc': "https://raw.githubusercontent.com/el-cms/Open-trivia-database/refs/heads/master/en/todo/uncategorized.json"
}

def getUserInfo(user_id):
    for user in all_users:
        if user.get("id") == user_id:
            return user
    return -1


def curlPostAI(prompt):
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, 'http://localhost:11434/api/generate')
  curl.setopt(pycurl.POST, 1)
  data = json.dumps({
      'model': 'gemma3:27b',
      'prompt': prompt,
      'options': {
          'temperature': 0.9,
          'top_p': 0.9,
          'repeat_penalty': 1.2,
          'top_k': 40
      },
      'stream': False,
  })
  curl.setopt(pycurl.HTTPHEADER, [
    'Content-Type: application/json',
    'Cache-Control: no-cache',
    'Pragma: no-cache'
  ])
  curl.setopt(pycurl.POSTFIELDS, data)
  buffer = BytesIO()
  curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
  curl.perform()
  response_body = json.loads(buffer.getvalue().decode('utf-8'))
  response_code = curl.getinfo(pycurl.RESPONSE_CODE)
  text = response_body['response'].replace('*', "")
  curl.close()
  return (text)
def clearChat():
  url = "http://localhost:11434/api/chat"
  payload = {
    "model": "gemma3:27b",
    "messages": []  # Empty array to reset context
  }
def curlPostAIO(prompt, model):
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, 'http://localhost:11434/api/generate')
  curl.setopt(pycurl.POST, 1)
  data = json.dumps({'model': model,
                     'prompt': prompt,
                     'stream': False})
  curl.setopt(pycurl.HTTPHEADER, [
    'Content-Type: application/json',
    'Cache-Control: no-cache',
    'Pragma: no-cache'
  ])
  curl.setopt(pycurl.POSTFIELDS, data)
  buffer = BytesIO()
  curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
  curl.perform()
  response_body = json.loads(buffer.getvalue().decode('utf-8'))
  response_code = curl.getinfo(pycurl.RESPONSE_CODE)
  text = response_body['response'].replace('*', "")
  curl.close()
  return (text)
def clearChatO():
  url = "http://localhost:11434/api/chat"
  payload = {
    "model": "gemma3:1b",
    "messages": []  # Empty array to reset context
  }
class BackendError(Exception):
    """Exception raised for errors in the backend API interactions."""
    pass
class ProntoUploader:
    def __init__(
        self,
        token: str,
        bubble_id: int,
        base_url: str = "https://stanfordohs.pronto.io",
        log_level: int = logging.INFO,
    ):
        self.base_url = base_url.rstrip("/")
        self.bubble_id = bubble_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s  %(levelname)-8s %(message)s",
            datefmt="%H:%M:%S",
        )
        self.log = logging.getLogger(self.__class__.__name__)

    def upload_file(self, path: str) -> dict:
        p = pathlib.Path(path)
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        size = p.stat().st_size
        url = f"{self.base_url}/api/files"
        params = {"filename": p.name, "normalize_image": "true"}
        headers = {**self.headers, "Content-Type": mime, "Content-Length": str(size)}

        with p.open("rb") as fh:
            r = requests.put(url, params=params, data=fh, headers=headers)
        r.raise_for_status()
        data = r.json()["data"]
        self.log.info("Uploaded %s → key=%s", p.name, data["key"])
        return data

    def wait_until_ready(
        self,
        orig_key: str,
        preset: str = "PHOTO",
        tries: int = 6,
        delay: float = 0.5,
    ) -> None:
        url = f"{self.base_url}/api/clients/files/{orig_key}/normalized"
        for attempt in range(1, tries + 1):
            r = requests.get(url, params={"preset": preset}, headers=self.headers)
            r.raise_for_status()
            if "normalized" in r.json().get("data", {}):
                self.log.info("✓ normalized (attempt %s)", attempt)
                return
            time.sleep(delay)
        self.log.warning("Normalization incomplete after %s attempts", tries)

    def create_message(
        self,
        orig_key: str,
        norm_key: str,
        meta: dict,
        text: str = "",
        media_type: str = "PHOTO",
        tries: int = 3,
    ) -> int:
        payload_stub = {"uuid": str(uuid.uuid4()), "bubble_id": self.bubble_id}
        url = f"{self.base_url}/api/v1/message.create"

        for attempt in range(1, tries + 1):
            payload = {
                **payload_stub,
                "message": text,
                "messagemedia": [
                    {
                        "mediatype": media_type,
                        "title": meta["name"],
                        "filesize": meta["filesize"],
                        "mimetype": meta["mimetype"],
                        "width": meta["width"],
                        "height": meta["height"],
                        "uuid": norm_key,
                    }
                ],
            }
            r = requests.post(url, json=payload, headers=self.headers)

            if r.status_code == 400 and "INVALID_ATTACHMENT_FILE_KEY" in r.text:
                self.log.warning(
                    "Key not ready (%s/%s), retrying…", attempt, tries
                )
                self.wait_until_ready(orig_key, tries=3, delay=0.7)
                continue

            r.raise_for_status()
            msg_id = r.json()["message"]["id"]
            self.log.info("✓ posted – message_id=%s", msg_id)
            return msg_id

        raise RuntimeError("Message creation failed after retries")

    def send(self, file_path: str, text: str = "") -> int:
        """
        Uploads a file, waits for normalization, and creates a message.
        Returns the message ID.
        """
        # 1. upload and determine original key
        info = self.upload_file(file_path)
        orig_key = info["key"]

        # 2. detect media category from local file or returned metadata
        mime = mimetypes.guess_type(file_path)[0] or ""
        category = mime.split("/", 1)[0]
        # map to Pronto preset/mediatype
        type_map = {"image": "PHOTO", "video": "VIDEO", "audio": "AUDIO"}
        preset = type_map.get(category, "PHOTO")

        # 3. wait for normalization under the chosen preset
        self.wait_until_ready(orig_key, preset=preset)

        # 4. fetch normalized metadata
        r = requests.get(
            f"{self.base_url}/api/clients/files/{orig_key}/normalized",
            params={"preset": preset},
            headers=self.headers,
        )
        r.raise_for_status()
        norm_data = r.json()["data"]["normalized"]

        # 5. prepare meta dict
        meta = {
            "name":     norm_data["name"],
            "filesize": norm_data["filesize"],
            "mimetype": norm_data["mimetype"],
            "width":    norm_data.get("width"),
            "height":   norm_data.get("height"),
        }

        # 6. create message with appropriate media_type
        return self.create_message(orig_key, norm_data["key"], meta, text, media_type=preset)
class StoredMessage:
    """Class to store message data including content, flags, and timestamp."""
    def __init__(self, message=" ", flags_in_message=0, timestamp=datetime.min):
        self.message = message
        self.flags_in_message = flags_in_message
        self.timestamp = timestamp
async def keep_alive(websocket, interval=30):
    """Sends a ping event periodically to keep the connection alive."""
    try:
        while True:
            ping_message = json.dumps({"event": "pusher:ping", "data": {}})
            await websocket.send(ping_message)
            await asyncio.sleep(interval)
    except websockets.exceptions.ConnectionClosedOK:
        # Connection closed normally
        logger.info("WebSocket connection closed cleanly")
    except websockets.exceptions.ConnectionClosedError as e:
        # Unexpected disconnection
        logger.error(f"WebSocket connection closed unexpectedly: {e}")

    except Exception as e:
        # Catch-all for other issues
        logger.error(f"Error in keep-alive: {e}")



class PollBot:
    """Main bot class for managing polls, games and commands."""
    
    def __init__(self, overthrowers):
        self.access_token = getAccesstoken()
        self.pending_banishes = {}
        self.pending_unbanishes = {}
        self.warning_count = []
        self.settings = [1, 1, 1, 1, 1]
        self.banished = []
        self.is_bot_owner = False
        self.bubble_owners = []
        self.main_bot = MainBot(MAIN_BUBBLE_ID, overthrowers)
        self.process_messages = True
        self.last_activity_time = datetime.min
        self.stored_messages = []
        self.events = []
        self.beta_testers = [6056537, 5301921, 5301889]
        # Rules lists
        self.adminrules = []
        self.rules = []
        
        if MAIN_BUBBLE_ID == "3832006":
            self.adminrules.append("https://docs.google.com/document/d/1pYLhxWIXCVS49JT3aBVMjMlXQmPQbxkgjQjEXj87dSA/edit?tab=t.0")
            self.rules.append("https://docs.google.com/document/d/17PhM0JfKHGlqzJ0OBohS4GQEAuc-ea0accY-lGU6zzs/edit?usp=sharing")
    

    
    async def connect_and_listen(self, bubble_id, bubble_sid):
        """Connect to the websocket and listen for messages."""
        uri = "wss://ws-mt1.pusher.com/app/f44139496d9b75f37d27?protocol=7&client=js&version=8.3.0&flash=false"
        try:
            async with websockets.connect(uri) as websocket:
                response = await websocket.recv()
                logger.info(f"Received: {response}")



                    # Start keep-alive in the background

                asyncio.create_task(keep_alive(websocket))
                data = json.loads(response)
                if "data" in data:
                    inner_data = json.loads(data["data"])
                    socket_id = inner_data.get("socket_id", None)

                    data = {
                        "event": "pusher:subscribe",
                        "data": {
                            "channel": f"private-bubble.{bubble_id}.{bubble_sid}",
                            "auth": self.main_bot.client.chat_auth(bubble_id, bubble_sid, socket_id)
                        }
                    }
                    await websocket.send(json.dumps(data))

                    if socket_id:
                        logger.info(f"Socket ID: {socket_id}")
                    else:
                        logger.warning("Socket ID not found in response")

                # Listen for incoming messages
                async for message in websocket:
                    if message == "ping":
                        await websocket.send("pong")
                    else:
                        try:
                            msg_data = json.loads(message)
                            event_name = msg_data.get("event", "")
                            if event_name == "pusher:ping":
                                await websocket.send(json.dumps({"event": "pusher:pong", "data": {}}))
                            if event_name == "App\\Events\\MessageAdded":
                                msg_content = json.loads(msg_data.get("data", "{}"))
                                msg = msg_content.get("message", {})

                                await self.main_bot.process_message(
                                    msg.get("message", ""),
                                    msg.get("user", {}).get("firstname", "Unknown"),
                                    msg.get("user", {}).get("lastname", "User"),
                                    datetime.strptime(msg.get("created_at", ""), "%Y-%m-%d %H:%M:%S"),
                                    msg.get("messagemedia", []),
                                    msg.get("user", {}).get("id", "User"),
                                    msg.get("id", "")
                                )
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            # Allow the main loop to handle reconnection


async def handle_status(request):
    """Handler for the status endpoint."""
    return web.Response(text="Bot is running!", status=200)

async def main_loop():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "overthrowlist.txt")
    global overthrowlist
    try:
        with open(file_path, "r", encoding="utf-8") as openfile:
            # Reading from json file
            overthrowlist = [int(line) for line in openfile]
    except Exception as e:
        print(e)
        overthrowlist = []


    # Create and initialize the bot
    bot = PollBot(overthrowlist)
    # Get bubble info and owners
    bubble_info = get_bubble_info(bot.access_token, int(MAIN_BUBBLE_ID))

    bot.bubble_owners = [row["user_id"] for row in bubble_info["bubble"]["memberships"] if row["role"] == "owner"]
    
    if USER_ID in bot.bubble_owners:
        bot.is_bot_owner = True
    
    bubble_sid = bubble_info["bubble"]["channelcode"]
    logger.info(f"Connecting to bubble with SID: {bubble_sid}")

    # Run the WebSocket logic with automatic reconnection
    while True:
        try:
            await bot.connect_and_listen(int(MAIN_BUBBLE_ID), bubble_sid)
        except Exception as e:
            logger.error(f"Connection error: {e}")
            # Wait before reconnecting
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")

# The above code was originally written by Taylan Derstadt, and further optomized by Paul Estrada (https://github.com/Society451)
# before OHS Tech and Pronto Team review on 4/9/2025-4/10/2025