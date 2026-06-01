# ================= IMPORTS =================

# Open and close desktop applications
from AppOpener import close, open as appopen

# Open URLs in browser
from webbrowser import open as webopen
import webbrowser

# Google and YouTube actions
from pywhatkit import search, playonyt

# Environment variables
from dotenv import dotenv_values

# Rich printing
from rich import print

# AI model
from groq import Groq

# System modules
import subprocess
import requests
import keyboard
import asyncio
import os


# ================= LOAD ENV VARIABLES =================

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


# ================= AI CLIENT =================

client = Groq(api_key=GroqAPIKey)


# ================= CHATBOT SETTINGS =================

professional_responses = [
    "Your satisfaction is my top priority.",
    "I'm at your service for any questions."
]

messages = []

SystemChatBot = [{
    "role": "system",
    "content":
    f"""
    Hello, I am {os.environ.get('Username', 'User')}.
    
    You are a content writer.
    
    Write engaging and professional content.
    
    Always provide accurate information.
    
    If unsure, say you don't know.
    """
}]


# ================= GOOGLE SEARCH =================

def GoogleSearch(topic):

    search(topic)

    return True


# ================= CONTENT CREATION =================

def Content(topic):

    # Open file in notepad
    def OpenNotepad(file):

        subprocess.Popen(
            ["notepad.exe", file]
        )

    # AI content generation
    def ContentWriterAI(prompt):

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=SystemChatBot + messages,

            max_tokens=2048,

            temperature=0.7,

            top_p=1,

            stream=True
        )

        answer = ""

        for chunk in completion:

            if chunk.choices[0].delta.content:

                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer

    # Remove "content" from input
    topic = topic.replace("Content ", "")

    content_by_ai = ContentWriterAI(topic)

    # Create filename
    filename = rf"Data\{topic.lower()}.txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content_by_ai)

    OpenNotepad(filename)

    return True


# ================= YOUTUBE SEARCH =================

def YouTubeSearch(topic):

    url = f"https://www.youtube.com/results?search_query={topic}"

    webbrowser.open(url)

    return True


# ================= PLAY YOUTUBE =================

def PlayYoutube(query):

    playonyt(query)

    return True


# ================= OPEN APP =================

def OpenApp(app):

    try:

        appopen(
            app,
            match_closest=True,
            output=True,
            throw_error=True
        )

        print(f"{app} opened locally")

        return True

    except:

        session = requests.Session()

        headers = {

            "User-Agent":
            "Mozilla/5.0"

        }

        app = app.lower().replace(" ", "")

        urls = [

            f"https://{app}.com",
            f"https://www.{app}.com",
            f"https://{app}.org",
            f"https://www.{app}.org",
            f"https://{app}.io",
            f"https://www.{app}.io",
            f"https://{app}.net"
        ]

        for url in urls:

            try:

                response = session.get(
                    url,
                    headers=headers,
                    timeout=3
                )

                if response.status_code < 400:

                    print(f"Opening {url}")

                    webopen(url)

                    return True

            except:
                continue

        print("No app found")

        return False


# ================= CLOSE APP =================

def CloseApp(app):

    if "chrome" in app:

        return False

    try:

        close(
            app,
            match_closest=True,
            output=True,
            throw_error=True
        )

        return True

    except:

        return False


# ================= SYSTEM CONTROL =================

def System(command):

    if command == "mute":

        keyboard.press_and_release(
            "volume mute"
        )

    elif command == "unmute":

        keyboard.press_and_release(
            "volume mute"
        )

    elif command == "volume up":

        keyboard.press_and_release(
            "volume up"
        )

    elif command == "volume down":

        keyboard.press_and_release(
            "volume down"
        )

    return True


# ================= COMMAND EXECUTION =================

async def TranslateAndExecute(commands):

    funcs = []

    for command in commands:

        # OPEN APP
        if command.startswith("open "):

            if "open it" in command:
                continue

            elif command == "open file":
                continue

            else:

                fun = asyncio.to_thread(
                    OpenApp,
                    command.removeprefix("open ")
                )

                # FIX:
                # Add task into list
                funcs.append(fun)

        # CLOSE APP
        elif command.startswith("close "):

            fun = asyncio.to_thread(
                CloseApp,
                command.removeprefix("close ")
            )

            funcs.append(fun)

        # PLAY YOUTUBE
        elif command.startswith("play "):

            fun = asyncio.to_thread(
                PlayYoutube,
                command.removeprefix("play ")
            )

            funcs.append(fun)

        # CONTENT
        elif command.startswith("content "):

            fun = asyncio.to_thread(
                Content,
                command.removeprefix("content ")
            )

            funcs.append(fun)

        # GOOGLE SEARCH
        elif command.startswith("google search "):

            fun = asyncio.to_thread(
                GoogleSearch,
                command.removeprefix(
                    "google search "
                )
            )

            funcs.append(fun)

        # YOUTUBE SEARCH
        elif command.startswith("youtube search "):

            fun = asyncio.to_thread(
                YouTubeSearch,
                command.removeprefix(
                    "youtube search "
                )
            )

            funcs.append(fun)

        # SYSTEM COMMANDS
        elif command.startswith("system "):

            fun = asyncio.to_thread(
                System,
                command.removeprefix(
                    "system "
                )
            )

            funcs.append(fun)

        else:

            print(
                f"No function for: {command}"
            )

    # Execute all tasks together
    results = await asyncio.gather(*funcs)

    for result in results:

        yield result


# ================= MAIN AUTOMATION =================

async def Automation(commands):

    async for result in TranslateAndExecute(commands):

        pass

    return True


# ================= START =================

if __name__ == "__main__":

    asyncio.run(

        Automation(
            [
                "open facebook",
                "open instagram",
                "play hanuman chalisa"
            ]
        )

    )