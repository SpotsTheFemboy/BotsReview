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

from ProcessScripts.banbot import BanBot

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
import base64
global mewmode
mewmode = 0
global emojimode
emojimode = 0
global superemojibanish
superemojibanish = 0
global inviters
inviters = []
# Setup logging
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
MAIN_BUBBLE_ID = "3832006"
LOG_CHANNEL_ID = "4283367"
admin_bubble_id = "4206470"
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

class BallsdexManager:
    """Manages the Ballsdex collection game."""

    def __init__(self):
        self.user_collections = {}  # user_id -> set of balls
        self.last_catch_times = {}  # user_id -> datetime
        self.cooldown = timedelta(seconds=10)

        # Just a few example balls – you can load these from a file later
        self.all_balls = [
            {"name": "Polandball", "rarity": "Common"},
            {"name": "Americaball", "rarity": "Uncommon"},
            {"name": "Soviet Onion", "rarity": "Rare"},
            {"name": "DogeBall", "rarity": "Epic"},
            {"name": "Holy Roman Empireball", "rarity": "Legendary"},
            {"name": "Cheeseball", "rarity": "Common"},
            {"name": "Voidball", "rarity": "Mythic"}
        ]

    def catch_ball(self, user_id):
        """Attempt to catch a new ball."""
        now = datetime.now()
        last_time = self.last_catch_times.get(user_id, datetime.min)

        if now - last_time < self.cooldown:
            seconds_left = int((self.cooldown - (now - last_time)).total_seconds())
            return None, f"Slow down! You can try again in {seconds_left} seconds."

        self.last_catch_times[user_id] = now

        new_ball = random.choice(self.all_balls)
        user_collection = self.user_collections.setdefault(user_id, set())
        already_had = new_ball["name"] in user_collection

        user_collection.add(new_ball["name"])

        if already_had:
            return f"You found a **{new_ball['name']}** ({new_ball['rarity']})... but you already had it!", None
        else:
            return f"You caught a **new** ball: **{new_ball['name']}** ({new_ball['rarity']})! 🎉", None

    def get_collection(self, user_id):
        """Return the user's current ball collection."""
        collection = self.user_collections.get(user_id)
        if not collection:
            return None, "You haven't caught any balls yet! Use `!catchball` to start collecting."

        formatted = ", ".join(sorted(collection))
        return f"Your Ballsdex: {formatted}", None


class HangmanManager:
    """Manages a hangman game."""

    def __init__(self):
        self.game_active = False
        self.game_master = None
        self.word = None
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.word_list = ["python", "hangman", "banana", "algorithm", "matrix"]

    def start_game(self, user_id):
        """Start a new hangman game."""
        if self.game_active:
            return None, "A game is already running."

        self.game_master = user_id
        self.word = random.choice(self.word_list)
        self.guessed_letters = set()
        self.remaining_attempts = 6
        self.game_active = True

        return self._get_display_word(), None

    def guess_letter(self, user_id, letter):
        """Process a letter guess."""
        if not self.game_active:
            return None, "No active hangman game."

        if user_id != self.game_master:
            return None, "You didn't start the current game."

        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            return None, "Please guess a single letter."

        if letter in self.guessed_letters:
            return None, "You already guessed that letter."

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.remaining_attempts -= 1

        if self._is_word_guessed():
            completed_word = self.word
            self._end_game()
            return f"You won! The word was **{completed_word}**", None

        if self.remaining_attempts <= 0:
            answer = self.word
            self._end_game()
            return f"You lost! The word was **{answer}**", None

        return self._get_display_word(), None

    def _get_display_word(self):
        """Return the current state of the word with blanks and guesses."""
        display = " ".join([ch if ch in self.guessed_letters else "_" for ch in self.word])
        return f"Word: {display} | Attempts left: {self.remaining_attempts}"

    def _is_word_guessed(self):
        """Check if the word has been fully guessed."""
        return all(letter in self.guessed_letters for letter in self.word)

    def _end_game(self):
        """Reset game state."""
        self.game_active = False
        self.game_master = None
        self.word = None
        self.guessed_letters.clear()
        self.remaining_attempts = 6


class TriviaManager:
    """Manages trivia games and questions."""

    def __init__(self):
        self.trivia_active = False
        self.trivia_master = None
        self.current_question = None
        self.trivia_categories = {}
        self.all_questions = []

    def load_trivia_data(self):
        """Load trivia data from URLs."""
        for category, url in TRIVIA_URLS.items():
            questions = self.download_questions(url)
            if questions:
                self.trivia_categories[category] = questions
                self.all_questions.extend(questions)

        logger.info(
            f"Loaded {len(self.all_questions)} trivia questions across {len(self.trivia_categories)} categories")

    def download_questions(self, url):
        """Download trivia questions from the given URL."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                lines = text.split("\n")
                questions = []
                for line in lines:
                    if line.strip():
                        # Remove trailing comma if present
                        if line.endswith(','):
                            line = line[:-1]
                        try:
                            question_data = json.loads(line)
                            questions.append(question_data)
                        except json.JSONDecodeError:
                            pass
                return questions
            else:
                logger.error(f"Failed to download questions from {url}: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error downloading questions from {url}: {e}")
            return []

    def start_trivia(self, user_id):
        """Start a new trivia game."""
        if not self.trivia_active:
            self.trivia_active = True
            self.trivia_master = user_id

            if not self.all_questions:
                self.load_trivia_data()

            if not self.all_questions:
                self.trivia_active = False
                return None, "Failed to load trivia questions"

            question_data = random.choice(self.all_questions)
            self.current_question = question_data
            return question_data['question'].capitalize(), None
        else:
            return None, "A trivia game is already active"

    def reveal_answer(self, user_id, bubble_owners):
        """Reveal the answer to the current trivia question."""
        if not self.trivia_active:
            return None, "No trivia game is currently active"

        if user_id != self.trivia_master and user_id not in bubble_owners:
            return None, "You don't have permission to reveal the answer"

        answers = self.current_question['answers']
        formatted_answers = ", ".join([answer.capitalize() for answer in answers])

        self.trivia_active = False
        self.trivia_master = None
        self.current_question = None

        return formatted_answers, None


class NumberGameManager:
    """Manages number guessing games."""

    def __init__(self):
        self.game_active = False
        self.correct_number = 0
        self.max_number = 0

    def start_game(self, max_num):
        """Start a new number guessing game."""
        if self.game_active:
            return False, "A game is already in progress"

        try:
            max_num = int(max_num)
        except ValueError:
            return False, "Invalid maximum number"

        if max_num < 1 or max_num > 10000:
            return False, "Maximum number must be between 1 and 10000"

        self.game_active = True
        self.max_number = max_num
        self.correct_number = random.randint(1, max_num)

        return True, f"I've chosen a number between 1 and {max_num}. Use !guess to make your guess!"

    def make_guess(self, guess):
        """Process a guess in the number game."""
        if not self.game_active:
            return False, "No number game is currently active"

        try:
            guess_num = int(guess)
        except ValueError:
            return False, "Invalid guess. Please enter a number"

        if guess_num < 1 or guess_num > self.max_number:
            return False, f"Your guess must be between 1 and {self.max_number}"

        if guess_num == self.correct_number:
            self.game_active = False
            return True, f"Correct! The answer was {guess_num}!"
        elif guess_num > self.correct_number:
            return False, f"{guess_num} is too high!"
        else:
            return False, f"{guess_num} is too low!"


class ProntoClient:
    """Handles communication with the Pronto API."""

    def __init__(self, api_base_url, access_token):
        self.api_base_url = api_base_url
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        self.stored_dms = []

    def send_message(self, message, bubble_id, media):
        """Send a message to a specific bubble."""
        if media is None:
            media = []

        unique_uuid = str(uuid.uuid4())
        message_created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "id": "Null",
            "uuid": unique_uuid,
            "bubble_id": bubble_id,
            "message": message,
            "created_at": message_created_at,
            "user_id": USER_ID,
            "attachment_file_keys": media
        }
        url = f"{self.api_base_url}api/v1/message.create"

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message: {e}")
            raise BackendError(f"Failed to send message: {e}")

    def get_dm_or_create(self, user_id):
        """Get an existing DM or create a new one with the specified user."""
        matches = [row for row in self.stored_dms if row[0] == user_id]
        if not matches:
            dm_info = createDM(self.access_token, user_id, ORG_ID)
            data = [user_id, dm_info]
            self.stored_dms.append(data)
            matches = [data]
        return matches[0][1]

    def chat_auth(self, bubble_id, bubble_sid, socket_id):
        """Authenticate for chat websocket connection."""
        url = f"{self.api_base_url}api/v1/pusher.auth"
        data = {
            "socket_id": socket_id,
            "channel_name": f"private-bubble.{bubble_id}.{bubble_sid}"
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            bubble_auth = response.json().get("auth")
            logger.info("Bubble Connection Established.")
            return bubble_auth
        except Exception as e:
            logger.error(f"Error authenticating chat: {e}")
            raise BackendError(f"Failed to authenticate chat: {e}")

    def upload_file_and_get_key(self, file_path, filename):
        """Upload a file to Pronto and get the file key."""
        url = "https://api.pronto.io/api/files"
        try:
            # Open the file and prepare headers
            with open(file_path, 'rb') as file:
                file_content = file.read()

            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
                "Content-Length": str(len(file_content)),
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "application/octet-stream"
            }

            # Send the PUT request
            response = requests.put(url, headers=headers, data=file_content)

            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                file_key = response_data['data']['key']
                return file_key
            else:
                logger.error(f"Failed to upload file: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return None
class MainBot:
    """Main bot class for managing polls, games and commands."""

    def __init__(self, main_bubble, overthrowers):
        self.access_token = getAccesstoken()
        self.client = ProntoClient(API_BASE_URL, self.access_token)
        self.trivia = TriviaManager()
        self.number_game = NumberGameManager()
        self.pending_banishes = {}
        self.pending_unbanishes = {}
        self.warning_count = []
        self.settings = [1, 1, 1, 1, 1]
        self.banished = []
        self.is_bot_owner = False
        self.bubble_owners = []
        self.overthrowlist = overthrowers
        self.bans = []
        global MAIN_BUBBLE_ID
        MAIN_BUBBLE_ID = main_bubble
        self.banbot = BanBot(MAIN_BUBBLE_ID)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.process_messages = True
        self.last_activity_time = datetime.min
        self.stored_messages = []
        self.events = []
        self.beta_testers = [6056537, 5301889]
        # Rules lists

        self.adminrules = []
        self.rules = []
        self.dead = []
        self.cooldowns = []
        if MAIN_BUBBLE_ID == "3832006":
            self.adminrules.append(
                "https://docs.google.com/document/d/1pYLhxWIXCVS49JT3aBVMjMlXQmPQbxkgjQjEXj87dSA/edit?tab=t.0")
            self.rules.append(
                "https://docs.google.com/document/d/17PhM0JfKHGlqzJ0OBohS4GQEAuc-ea0accY-lGU6zzs/edit?usp=sharing")
        self.start()
    def start(self):
        self.client.send_message("Everyone has been revived!", MAIN_BUBBLE_ID, [])
    async def process_message(self, msg_text, user_firstname, user_lastname, timestamp, msg_media, user_id, msg_id):
        """Process an incoming message."""
        # Check for bot toggling command
        if msg_text.startswith("!bot"):
            command = msg_text[1:].split()
            print(command)
            if len(command) > 1 and (user_id == INT_USER_ID):
                if command[1] == "on":
                    self.process_messages = True
                    logger.info(f"Bot enabled by {user_id}")
                    send_reaction(accesstoken, '💡', msg_id)
                elif command[1] == "off":
                    self.process_messages = False
                    logger.info(f"Bot disabled by {user_id}")
                    send_reaction(accesstoken, '📴', msg_id)

        if not self.process_messages:
            return


        if user_id not in self.banished or user_id == INT_USER_ID:
            await self.check_for_commands(msg_text, user_id, user_firstname, user_lastname, timestamp, msg_id)



    def check_cooldown(self, user_id):
        print(self.cooldowns)

        for index, person in enumerate(self.cooldowns):
            if person['user_id'] == user_id:
                if (datetime.now() - person['time']).total_seconds() > 5:
                    self.cooldowns[index]['time'] = datetime.now()
                    return True
                return False

        # If user not found, add them to cooldowns
        self.cooldowns.append({'user_id': user_id, 'time': datetime.now()})
        return True


    async def check_for_commands(self, msg_text_tall, user_id, user_firstname, user_lastname, timestamp, msg_id, media=None):
        """Check for commands in the message and handle them."""
        if media is None:
            media = []

        chat = self.client.get_dm_or_create(user_id)['bubble']['id']
        msg_text = msg_text_tall.lower()
        command = msg_text[1:].split()
        command2 = msg_text_tall[1:].split()  # Preserves case

        global ratelimit
        if msg_text.startswith("!revive") and user_id in self.beta_testers:
            self.dead = []
            send_reaction(accesstoken, "🙏", msg_id)
        if msg_text.startswith("!battle"):
            if user_id not in self.dead:
                if self.check_cooldown(user_id):
                    target_match = re.search(r"<@(\d+)>", command[1])
                    if target_match:
                        target_user = int(target_match.group(1))
                        if target_user not in self.dead:
                            ratelimit = datetime.now()
                            number = random.randint(1, 20)
                            killnums = [1,2,3,4]
                            if number in killnums:
                                emoji = "🏆"
                                self.dead.append(target_user)
                            elif number == 5:
                                emoji = "🥈"
                                self.dead.append(user_id)
                            else:
                                emoji = "🛡️"

                            try:
                                send_reaction(accesstoken, emoji, msg_id)
                            except Exception as e:
                                if e.__str__().startswith(
                                        "HTTP error occurred: 422 Client Error: Unprocessable Content for url:"):
                                    emoji = emoji.strip("\n")
                                    emoji = emoji + '️'
                                    try:
                                        send_reaction(accesstoken, emoji, msg_id)
                                    except Exception as e:
                                        if e.__str__().startswith(
                                                "HTTP error occurred: 422 Client Error: Unprocessable Content for url:"):
                                            logger.error(e)
                                            send_reaction(accesstoken, "❌", msg_id)

        if msg_text.startswith("!smite") and user_id == INT_USER_ID:
            target_match = re.search(r"<@(\d+)>", command[1])
            if target_match:
                target_user = int(target_match.group(1))
                if target_user not in self.dead:
                    ratelimit = datetime.now()
                    emoji = "⚡"
                    self.dead.append(target_user)


                    try:
                        send_reaction(accesstoken, emoji, msg_id)
                    except Exception as e:
                        if e.__str__().startswith(
                                "HTTP error occurred: 422 Client Error: Unprocessable Content for url:"):
                            emoji = emoji.strip("\n")
                            emoji = emoji + '️'
                            try:
                                send_reaction(accesstoken, emoji, msg_id)
                            except Exception as e:
                                if e.__str__().startswith(
                                        "HTTP error occurred: 422 Client Error: Unprocessable Content for url:"):
                                    logger.error(e)
                                    send_reaction(accesstoken, "❌", msg_id)

            if msg_text.startswith("!banish") and (user_id == INT_USER_ID):
                target_match = re.search(r"<@(\d+)>", command[1])
                if target_match:
                    target_user = int(target_match.group(1))
                    self.banished.append(target_user)
                    logger.info(f"User {target_user} banished by {user_id}")
                    self.client.send_message(f"User <@{target_user}> has been banished.", chat, [])

            elif msg_text.startswith("!unbanish") and (user_id == INT_USER_ID):
                target_match = re.search(r"<@(\d+)>", command[1])
                if target_match:
                    target_user = int(target_match.group(1))
                    if target_user in self.banished:
                        self.banished.remove(target_user)
                        logger.info(f"User {target_user} unbanished by {user_id}")
                        self.client.send_message(f"User <@{target_user}> has been unbanished.", chat, [])
                    else:
                        self.client.send_message(f"User <@{target_user}> is not banished.", chat, [])