#Author: Paul Estrada
#Email: paul257@ohs.stanford.edu
#URL: https://github.com/Society451/Better-Pronto

import os

def createappfolders():
    base_path = os.path.expanduser("~/.bpro")
    data_path = os.path.join(base_path, "data")
    client_path = os.path.join(base_path, "client")
    auth_path = os.path.join(data_path, "auth")
    chats_path = os.path.join(data_path, "chats")
    bubbles_path = os.path.join(chats_path, "bubbles")  # New folder path
    users_path = os.path.join(data_path, "users")  # New folder path
    loginTokenJSONPath = os.path.join(auth_path, "loginToken.json")
    authTokenJSONPath = os.path.join(auth_path, "authToken.json")
    verificationCodeResponseJSONPath = os.path.join(auth_path, "verificationCoderesponse.json")
    settings_path = os.path.join(client_path, "settings")
    encryption_path = os.path.join(client_path, "encryption")
    logs_path = os.path.join(client_path, "logs")
    settingsJSONPath = os.path.join(settings_path, "settings.json")
    keysJSONPath = os.path.join(encryption_path, "keys.json")
    bubbleOverviewJSONPath = os.path.join(chats_path, "bubbleOverview.json")
    os.makedirs(auth_path, exist_ok=True)
    os.makedirs(chats_path, exist_ok=True)
    os.makedirs(bubbles_path, exist_ok=True)  # Create the new folder
    os.makedirs(users_path, exist_ok=True)  # Create the new folder
    os.makedirs(settings_path, exist_ok=True)
    os.makedirs(encryption_path, exist_ok=True)
    os.makedirs(logs_path, exist_ok=True)



    return auth_path, chats_path, bubbles_path, loginTokenJSONPath, authTokenJSONPath, verificationCodeResponseJSONPath, settings_path, encryption_path, logs_path, settingsJSONPath, keysJSONPath, bubbleOverviewJSONPath, users_path