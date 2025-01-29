import requests
import time
import websockets
import asyncio
import random
import json
import sys
import os
import socket

#usernames = ["random_elf", "random_knight", "document_dragon", "spreadsheet_sorcerer", "chart_crusader", "table_troll", "paragraph_paladin", "formatting_fairy", "hyperlink_hero"] 
username = ""
# URL to make the GET request to
# Create a dummy connection to determine the LAN IP

local_ip = os.environ['LOCAL_IP']

base_url = f"http://{local_ip}:4200"#"https://overflowapp.xyz:4200" #"http://localhost:4500"#
add_to_queue_url = f"{base_url}/api/addtoqueue"
signin_url = f"{base_url}/api/continueAsGuest"
socket_uri = f"ws://{local_ip}:4200/ws/"#"wss://overflowapp.xyz:4200/ws/" #"ws://localhost:4500/ws/"#
player_1 = ""
password = os.environ['PASSWORD']


def sleep_before_leave():
     # Generate a random duration between 2 and 6 seconds
     random_sleep_duration = random.uniform(2, 6)

     # Sleep for the random duration
     time.sleep(random_sleep_duration)

async def connect_and_communicate():
     # Replace with the WebSocket URL

    async with websockets.connect(socket_uri) as websocket:
        #print("Connected to WebSocket")

        # Continuously listen for messages and send messages
        last_message = ""
        while True:
            try:
                # Receive message
                message = await websocket.recv()
                #print("Received message:", message)

                if last_message == message:
                     exit(0)
                last_message = message
                # Send message
                if "0.1" in message:
                     #print("got board")
                     await websocket.send("opponent")
                elif "You lost" in message:
                     #print("I lost")
                     sleep_before_leave()
                     exit(0)   
                elif "start" in message:
                     #print("Timer message, discard")
                     pass
                elif "opponent" in message:
                     #print("Opponent connected")
                     #await websocket.send("opponent")
                     time.sleep(2)
                     if player_1 == username:
                         x = random.randint(0, 24)
                         y = random.randint(0, 24)
                         response = f"{x}:{y}"
                         #print("Sending random move", response)
                         await websocket.send(response)
                else:
                    #print("got position")
                    #print(message)
                    try:
                        array = json.loads(message)
                        #print("Got available moves, picking one and sending")
                        if len(array) == 0:
                             #print("I lost")
                             sleep_before_leave()
                             exit(0)
                        move_index = random.randint(0, len(array) - 1)
                        x = array[move_index]["X"]
                        y = array[move_index]["Y"]
                        response = f"{x}:{y}"
                        
                        #print("picked: ", response)
                        time.sleep(3)
                        await websocket.send(response)

                    except json.JSONDecodeError:
                         if message == "You won":
                              #print("I won")
                              sleep_before_leave()
                              exit(0)
                         if message == "You lost":
                              #print("I won")
                              sleep_before_leave()
                              exit(0)
                         if message == "Player 1 ran out of time":
                              #print("Player 1 ran out of time")
                              sleep_before_leave()
                              exit(0)
                         if message == "Player 2 ran out of time":
                              #print("Player 2 ran out of time")
                              sleep_before_leave()
                              exit(0)
                         #print("Got opponent move, my turn now")
                         x = random.randint(0, 24)
                         y = random.randint(0, 24)
                         response = f"{x}:{y}"
                         #print("Sending random move", response)
                         await websocket.send(response)
                
                #print("Message sent successfully ", response)

            except websockets.ConnectionClosed:
                #print("WebSocket connection closed")
                break

def signinGuest():
    global username
    body = {
    "isBot": True,
     }
    response = requests.post(signin_url, json=body)
    singin_response_json = response.json()
    if response.status_code == 200 and singin_response_json["isSuccess"] == True:
        data = singin_response_json["data"]
        bearer = data["bearerToken"]
        username = data["username"]
        #print('sign in success ', username)
        #print("Got bearer token ", bearer)
        data = {"username": username}
        #print("Posting data ", add_to_queue_url)
        headers = {
        'Authorization': f'Bearer {bearer}',
        'GameVersion': '10.0.0'
        }
        return headers
    return None

# Sending the GET request
#print("LAUNCHED BOT")
headers = signinGuest()
if headers != None:
    data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
     }
    response = requests.post(add_to_queue_url, headers=headers, json=data)
    
    if response.status_code == 200:
            # Printing the response content
            #print("Response content:")
            #print(response.text)
            response_json =  response.json()
            if response_json["isSuccess"] == True:
                #print("added to queue ", username)
                get_my_match_url = f"{base_url}/api/getMyMatch?username={username}"
                while True:
                        #print('getting match for username ', username)
                        response = requests.get(get_my_match_url, headers=headers)
                        #print(response.text)
                        if response.status_code == 200:
                            response_json = response.json()
                            data =  response_json["data"]
                            #print("Got data from match" , data)
                            if data is not None and data["player1"] is not None and data["player2"] is not None:
                                #print("Found match")
                                players = f'{data["player1"]}-{data["player2"]}'
                                gameId = data["gameId"]
                                player_1 = data["player1"]
                                socket_uri += f"{gameId}/{players}/{username}"
                                asyncio.run(connect_and_communicate())
                                break
                        else:
                             #print("get my match did not return 200")
                             headers = signinGuest()
                             if headers is None:
                                  #print("Bearer expired and cant sign in again ", username, password)
                                  exit(0)
                        time.sleep(5)
    else:
        # If the request failed, print an error message
        print(f"Error adding to queue: {response.status_code}")
        # Checking if the request was successful (status code 200)
else:
     print("Failed to login with credentials ", username, password) 
