# =========================================================
#              JARVIS REALTIME SEARCH ENGINE
# =========================================================
#
# Features:
#
# 1. Google Search Integration
# 2. Realtime AI Responses
# 3. Internet-Based Information
# 4. Chat Memory System
# 5. Streaming Responses
# 6. Realtime Date & Time
# 7. Search Result Injection
#
# =========================================================



# =========================================================
#                IMPORT REQUIRED LIBRARIES
# =========================================================

# Google search library.
from googlesearch import search

# Groq AI SDK.
from groq import Groq

# Used for reading/writing JSON files.
from json import load, dump

# Used for realtime date & time.
import datetime

# Used for loading environment variables.
from dotenv import dotenv_values

# Rich terminal output.
from rich import print



# =========================================================
#              LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load variables from .env file.
env_vars = dotenv_values(
    "C:\\Users\\hp\\OneDrive\\Desktop\\jarvis_demo\\.env"
)

# Retrieve username.
Username = env_vars.get("Username")

# Retrieve assistant name.
Assistantname = env_vars.get("Assistantname")

# Retrieve Groq API key.
GroqAPIKey = env_vars.get("GroqAPIKey")



# =========================================================
#               INITIALIZE GROQ CLIENT
# =========================================================

# Create Groq client instance.
client = Groq(api_key=GroqAPIKey)



# =========================================================
#                 SYSTEM INSTRUCTIONS
# =========================================================

# Main assistant personality + behavior.
System = f"""

Hello, I am {Username}.

You are a very accurate and advanced AI chatbot
named {Assistantname}
which has real-time up-to-date information
from the internet.

*** Provide answers professionally. ***
*** Use proper grammar and punctuation. ***
*** Just answer from provided realtime data. ***

"""



# =========================================================
#               LOAD CHAT HISTORY
# =========================================================

# Attempt to load previous chat history.
try:

    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "r"
    ) as f:

        messages = load(f)

# Create empty chat history if file not found.
except:

    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "w"
    ) as f:

        dump([], f)



# =========================================================
#                GOOGLE SEARCH FUNCTION
# =========================================================

def GoogleSearch(query):

    """
    Perform Google search and
    collect top search results.
    """



    # =====================================================
    #               SEARCH GOOGLE
    # =====================================================

    results = list(
        search(
            query,
            advanced=True,
            num_results=5
        )
    )



    # =====================================================
    #             CREATE SEARCH RESPONSE
    # =====================================================

    Answer = f"The search results for '{query}' are:\n[start]\n"



    # =====================================================
    #             FORMAT SEARCH RESULTS
    # =====================================================

    for i in results:



        # Add title + description.
        Answer += (

            f"Title: {i.title}\n"

            f"Description: {i.description}\n\n"
        )



    # Ending tag.
    Answer += "[end]"



    return Answer



# =========================================================
#              RESPONSE CLEANING FUNCTION
# =========================================================

def AnswerModifier(Answer):

    """
    Remove empty lines from response.
    """



    # Split response into lines.
    lines = Answer.split('\n')



    # Remove blank lines.
    non_empty_lines = [

        line for line in lines

        if line.strip()
    ]



    # Rejoin cleaned lines.
    modified_answer = '\n'.join(non_empty_lines)



    return modified_answer



# =========================================================
#               SYSTEM CHAT HISTORY
# =========================================================

# Initial assistant setup.
SystemChatBot = [

    {
        "role": "system",
        "content": System
    },



    {
        "role": "user",
        "content": "Hi"
    },



    {
        "role": "assistant",
        "content": "Hello, how can I help you?"
    }
]



# =========================================================
#            REALTIME INFORMATION FUNCTION
# =========================================================

def Information():

    """
    Generate realtime date & time information.
    """



    # Empty data string.
    data = ""



    # Get current datetime.
    current_date_time = datetime.datetime.now()



    # Extract date & time components.
    day = current_date_time.strftime("%A")

    date = current_date_time.strftime("%d")

    month = current_date_time.strftime("%B")

    year = current_date_time.strftime("%Y")

    hour = current_date_time.strftime("%H")

    minute = current_date_time.strftime("%M")

    second = current_date_time.strftime("%S")



    # =====================================================
    #              FORMAT REALTIME DATA
    # =====================================================

    data += "Use This Real-time Information if needed:\n"

    data += f"Day: {day}\n"

    data += f"Date: {date}\n"

    data += f"Month: {month}\n"

    data += f"Year: {year}\n"

    data += (
        f"Time: {hour} hours, "
        f"{minute} minutes, "
        f"{second} seconds.\n"
    )



    return data



# =========================================================
#          REALTIME SEARCH ENGINE FUNCTION
# =========================================================

def RealtimeSearchEngine(prompt):

    """
    Main realtime internet-powered AI engine.
    """



    # Access global variables.
    global SystemChatBot, messages



    # =====================================================
    #               LOAD CHAT HISTORY
    # =====================================================

    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "r"
    ) as f:

        messages = load(f)



    # =====================================================
    #               STORE USER QUERY
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": f"{prompt}"
        }
    )



    # =====================================================
    #             ADD GOOGLE SEARCH RESULTS
    # =====================================================

    SystemChatBot.append(

        {
            "role": "system",

            "content": GoogleSearch(prompt)
        }
    )



    # =====================================================
    #             SEND REQUEST TO GROQ AI
    # =====================================================

    completion = client.chat.completions.create(

        # AI model name.
        model="llama-3.3-70b-versatile",



        # System prompt + realtime info + memory.
        messages=

        SystemChatBot

        + [
            {
                "role": "system",
                "content": Information()
            }
        ]

        + messages,



        # Creativity level.
        temperature=0.7,



        # Maximum response size.
        max_tokens=2048,



        # Nucleus sampling.
        top_p=1,



        # Enable streaming.
        stream=True,



        # No stopping condition.
        stop=None
    )



    # =====================================================
    #                STORE FINAL ANSWER
    # =====================================================

    Answer = ""



    # =====================================================
    #             RECEIVE STREAMED RESPONSE
    # =====================================================

    for chunk in completion:



        # Check if chunk contains text.
        if chunk.choices[0].delta.content:



            # Append generated chunk.
            Answer += chunk.choices[0].delta.content



    # =====================================================
    #                CLEAN RESPONSE
    # =====================================================

    Answer = Answer.strip().replace("</s>", "")



    # =====================================================
    #              SAVE ASSISTANT RESPONSE
    # =====================================================

    messages.append(

        {
            "role": "assistant",
            "content": Answer
        }
    )



    # =====================================================
    #                 SAVE CHAT LOG
    # =====================================================

    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "w"
    ) as f:

        dump(messages, f, indent=4)



    # =====================================================
    #         REMOVE TEMPORARY SEARCH RESULT
    # =====================================================

    SystemChatBot.pop()



    # =====================================================
    #             RETURN CLEAN RESPONSE
    # =====================================================

    return AnswerModifier(Answer=Answer)



# =========================================================
#                  MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":



    # Infinite assistant loop.
    while True:



        # Take user query.
        prompt = input(
            "Enter your query (or 'exit' to quit): "
        )



        # Exit condition.
        if prompt.lower() == "exit":

            break



        # Generate realtime AI response.
        response = RealtimeSearchEngine(prompt)



        # Print response.
        print(response)