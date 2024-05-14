import requests
import time
import websockets
import asyncio
import random
import json

username = "random_elf"
# URL to make the GET request to
base_url = "http://192.168.1.125:4500"
add_to_queue_url = f"{base_url}/api/addtoqueue"
get_my_match_url = f"{base_url}/api/getMyMatch?username={username}"
socket_uri = "ws://192.168.1.125:4500/ws/" 

async def connect_and_communicate():
     # Replace with the WebSocket URL

    async with websockets.connect(socket_uri) as websocket:
        print("Connected to WebSocket")

        # Continuously listen for messages and send messages
        while True:
            try:
                # Receive message
                message = await websocket.recv()
                print("Received message:", message)

                # Send message
                if "0.1" in message:
                     print("got board")
                elif "opponent" in message:
                     print("Opponent connected")
                     await websocket.send("opponent")
                else:
                    print("got position")
                    print(message)
                    try:
                        array = json.loads(message)
                        print("Got available moves, picking one and sending")
                        if len(array) == 0:
                             print("I lost")
                             exit(0)
                        move_index = random.randint(0, len(array) - 1)
                        x = array[move_index]["X"]
                        y = array[move_index]["Y"]
                        response = f"{x}:{y}"
                        
                        print("picked: ", response)
                        await websocket.send(response)

                    except json.JSONDecodeError:
                         if message == "You won":
                              print("I won")
                              exit(0)
                         print("Got opponent move, my turn now")
                         x = random.randint(0, 24)
                         y = random.randint(0, 24)
                         response = f"{x}:{y}"
                         print("Sending random move", response)
                         await websocket.send(response)
                
                #print("Message sent successfully ", response)

            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
                break


# Sending the GET request
data = {"username": username}
print("Posting data ", add_to_queue_url)
response = requests.post(add_to_queue_url, json=data)
if response.status_code == 200:
        # Printing the response content
        print("Response content:")
        print(response.text)
        response_json =  response.json()
        if response_json["isSuccess"] == True:
              
              while True:
                    response = requests.get(get_my_match_url)
                    print(response.text)
                    response_json = response.json()
                    data =  response_json["data"]
                    print("Got data from match" , data)
                    if data["player1"] is not None and data["player2"] is not None:
                        print("Found match")
                        game_id = f'{data["player1"]}-{data["player2"]}'
                        socket_uri = f"ws://192.168.1.125:4500/ws/{game_id}/{username}"
                        asyncio.run(connect_and_communicate())
                        break
                    time.sleep(2)
else:
    # If the request failed, print an error message
    print(f"Error: {response.status_code}")
    # Checking if the request was successful (status code 200)
    
