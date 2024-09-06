# Telegram bot to generate passwords

"""
Felix AI from the Hands and Knees Crew '24
- A Telegram bot
- Link: bit.ly/hkfelixai

Required modules
- python-telegram-bot
- pyfiglet
- duckduckgo-search
- python-dotenv
"""

import string
import random
import os
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime
from pyfiglet import Figlet
from time import sleep
from duckduckgo_search import DDGS
from dotenv import load_dotenv

f = Figlet(font="graffiti")

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "felixai_hkbot"
# USERNAME =

list_of_intro = ["Hello, how may i help you?", "Welcome!", "Hi! generate a random password for your social media accounts with one command", "Good day!"]


def gen_password(length=8, contains_symbols=False):
    our_string = list(string.ascii_letters + string.digits + string.punctuation)
    random.shuffle(our_string)
    # password = ""
    # for i in range(0, length):
    #     password = password + random.choice(chars)
    password = random.choices(our_string, k=length)
    icon = random.choice(['🔑', '🗝'])
    no_chars = f"_{length} characters_"
    return f'''{icon} Password:
    ```{''.join(password)}```
_{length} characters_
'''

def gen_username(text):
    return f"Username: {text}"

# Searching in Duckduckgo
def duck_search(text="Python Programming", max_results=3):
    results = DDGS().text(keywords=text, max_results=max_results)
    formatted_result = ""
    for each_result in results:
        formatted_result += f"""
*{each_result['title']}*
{each_result['body']}
_Link:_ {each_result['href']}
"""
    return formatted_result



# Menu
async def start_command(update:Update, context: ContextTypes):
    await update.message.reply_markdown(random.choice(list_of_intro))

async def help_command(update:Update, context: ContextTypes):
    await update.message.reply_markdown("""<h4>FelixAI can do alot</h4>
    - Generate password
    - DuckDuckGo Search""")

async def gen_password_command(update:Update, context: ContextTypes):
    try:
        update_length = int(update.message.text.replace("/gen_password", ""))
    except:
        update_length = 8
    await update.message.reply_markdown(gen_password(length=update_length))

# async def gen_username_command(update:Update, context: ContextTypes, text):
#     await update.message.reply_markdown(gen_username(text=text))

# for Duck_search
async def duck_search_command(update:Update, context: ContextTypes):
    if bool(update.message.text.replace("/duck_search", "").strip()):
        update_text = update.message.text.replace("/duck_search ", "")
    else:
        update_text = "Python programming"
    await update.message.reply_markdown(duck_search(update_text))

# Responses
def handle_response(text):
    text = text.lower()

    if text in ["hello", "hey", "yo"] or "hello" in text or "yo" in text:
        return f'''
        {random.choice(["Hello, how may i help you?", "Yo! what's good?", "Welcome!", "What's up homie?", "Wagwan"])}
        '''

    if "who am i" in text:
        return "The real question is *Who are you?*"

    if "date" in text and "time" in text:
        return f'The date and time today is _{datetime.now().ctime()}_'

    if "time" in text:
        return f'The date is _{datetime.now().strftime("%I:%M%p")}_'

    if "date" in text:
        return f'The time is _{datetime.now().strftime("%A %d %B %Y")}_'

    if "hk resources" in text:
        return "Hands and Knees AI Session Resources: **https://drive.google.com/drive/folders/1RFmPGMii1jVnbz66NAZzYnK2lAaC6A2O?usp=drive_link**"

    # Still need to fix this
    if text.startswith("!py"):
        return "(!) In progress: Running Python codes..."
        # return eval(text.replace("!py ", ""))

    # send a file
    # youtube

    return f"""I seem not to {random.choice(['dig', 'get', 'understand'])}\n{random.choice(['Try', 'Use', 'Type'])} the __help__ command
"""

async def handle_message(update: Update, context: ContextTypes):
    message_type = update.message.chat.type
    text = update.message.text

    print(f"[{message_type}] @{update.message.chat.username}({update.message.chat.id}): {text}")

    if message_type == "group" and BOT_USERNAME in text:
        text = text.replace(BOT_USERNAME, "")

    response = handle_response(text)
    print(f"{BOT_USERNAME}: {response}")

    await update.message.reply_markdown_v2(response)


async def error(update:Update, context: ContextTypes):
    await update.message.reply_markdown_v2(f"❌ Oops! an Error ocurred!\n{context.error}")
    print(f"(!) Alert: {update} caused an error {context.error}")


if __name__ == "__main__":
    print(f.renderText("FelixAI"))
    sleep(1.5)
    print("(+) Launching Felix...")

    app = Application.builder().token(TOKEN).build()

    # Adding our commands to the app
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("gen_password", gen_password_command))
    app.add_handler(CommandHandler("duck_search", duck_search_command, has_args=True))

    # Adding message handler to the app
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Adding error handler to the app
    app.add_error_handler(error)

    # Polling the bot
    print("(*) Polling...")
    app.run_polling(poll_interval=5)