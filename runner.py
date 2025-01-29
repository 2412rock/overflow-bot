import threading
import subprocess
import time

# Function to run a bot in a new thread
def run_bot(bot_name):
    while True:
        # Run the bot and wait for it to complete
        process = subprocess.Popen(["python", "bot.py", bot_name])
        process.wait()
        # Wait before restarting the bot
        time.sleep(2)

def run_bot_guest():
    while True:
        # Run the bot and wait for it to complete
        process = subprocess.Popen(["python", "guest_bot.py"])
        process.wait()
        # Wait before restarting the bot
        time.sleep(2)

# List of bot names
bot_names = ["random_bot", "Pixel", "Voyager", "Nebula", "Explorer", "Scribe"]

# Create and start a thread for each bot
threads = []
threads_guests = []
for bot_name in bot_names:
    thread = threading.Thread(target=run_bot, args=(bot_name,))
    thread.start()
    threads.append(thread)

for i in bot_names:
    thread = threading.Thread(target=run_bot_guest)
    thread.start()
    threads_guests.append(thread)

# Optional: Wait for all threads to complete (they won't in this example, since they run indefinitely)
for thread in threads:
    thread.join()
    
for thread in threads_guests:
    thread.join()