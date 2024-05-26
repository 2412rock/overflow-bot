import threading
import os, time
usernames = ["random_elf", "random_knight", "document_dragon", "spreadsheet_sorcerer", "chart_crusader", "table_troll", "paragraph_paladin", "formatting_fairy", "hyperlink_hero", "dodo"] 

def run_command(username):
    os.system(f"python bot.py {username}")

for username in range(1,200):
    thread = threading.Thread(target=run_command, args=(f'random_elf_{username}',))

    # Start the thread
    thread.start()
    #time.sleep(1)