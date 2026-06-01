# =========================================================
#                  JARVIS CHATBOT SYSTEM
# =========================================================
#
# Features:
# 1. AI Chatbot using Groq API
# 2. Real-Time Date & Time Information
# 3. Chat Memory Storage
# 4. Streaming AI Responses
# 5. Automatic Chat Log Saving
# 6. Error Handling + Recovery
#
# =========================================================



# =========================================================
#                IMPORT REQUIRED LIBRARIES
# =========================================================

# Groq AI SDK
from groq import Groq

# Used for reading/writing JSON files.
from json import load, dump

# Used for getting current date & time.
import datetime

# Used for loading environment variables.
from dotenv import dotenv_values



# =========================================================
#              LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load variables from .env file.
env_vars = dotenv_values(
    "C:\\Users\\hp\\OneDrive\\Desktop\\jarvis_demo\\.env"
)

# Retrieve username from .env.
Username = env_vars.get("Username")

# Retrieve assistant name from .env.
Assistantname = env_vars.get("Assistantname")

# Retrieve Groq API key from .env.
GroqAPIKey = env_vars.get("GroqAPIKey")



# =========================================================
#               INITIALIZE GROQ CLIENT
# =========================================================

# Create Groq AI client using API key.
client = Groq(api_key=GroqAPIKey)



# =========================================================
#                 SYSTEM INSTRUCTIONS
# =========================================================

# This system prompt controls assistant behavior.
System = f"""
Hello, I am {Username}.

You are a very accurate and advanced AI chatbot
named {Assistantname} with real-time information.

*** Do not tell time until I ask. ***
*** Do not talk too much, give concise answers. ***
*** Always reply in English. ***
*** Do not mention training data. ***
"""



# =========================================================
#              SYSTEM MESSAGE STRUCTURE
# =========================================================

# Convert system prompt into chatbot format.
SystemChatBot = [
    {
        "role": "system",
        "content": System
    }
]



# =========================================================
#                LOAD CHAT HISTORY
# =========================================================

# Try loading previous conversation history.
try:

    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "r"
    ) as f:

        messages = load(f)

# If chat log file does not exist.
except FileNotFoundError:

    # Create empty chat log file.
    with open(
        r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
        "w"
    ) as f:

        dump([], f)

    # Initialize empty messages list.
    messages = []



# =========================================================
#           REAL-TIME INFORMATION FUNCTION
# =========================================================

def RealtimeInformation():

    """
    Returns current real-time information.
    """

    # Get current system date & time.
    now = datetime.datetime.now()


    # Return formatted realtime information.
    return (

        "Real-time info:\n"

        f"Day: {now.strftime('%A')}\n"

        f"Date: {now.strftime('%d')}\n"

        f"Month: {now.strftime('%B')}\n"

        f"Year: {now.strftime('%Y')}\n"

        f"Time: {now.strftime('%H:%M:%S')}\n"
    )


# =========================================================
#             CLEAN AI RESPONSE FUNCTION
# =========================================================

def AnswerModifier(answer):

    """
    Remove empty lines from AI response.
    """

    return "\n".join(
        line for line in answer.split("\n")
        if line.strip()
    )



# =========================================================
#                 MAIN CHATBOT FUNCTION
# =========================================================

def ChatBot(query):

    """
    Main AI chatbot function.
    """
    try:

        # =================================================
        #              LOAD CHAT HISTORY
        # =================================================

        with open(
            r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
            "r"
        ) as f:

            messages = load(f)



        # =================================================
        #               STORE USER MESSAGE
        # =================================================

        messages.append(
            {
                "role": "user",
                "content": query
            }
        )



        # =================================================
        #               SEND REQUEST TO AI
        # =================================================

        completion = client.chat.completions.create(

            # AI model name.
            model="llama-3.1-8b-instant",

            # System prompt + realtime info + memory.
            messages=

            SystemChatBot

            + [
                {
                    "role": "system",
                    "content": RealtimeInformation()
                }
            ]

            + messages,


            # Maximum response size.
            max_tokens=1024,

            # Creativity level.
            temperature=0.7,

            # Nucleus sampling.
            top_p=1,

            # Enable streaming response.
            stream=True,
        )


        # =================================================
        #             RECEIVE STREAMED RESPONSE
        # =================================================

        # Empty response string.
        answer = ""

        # Process response chunks.
        for chunk in completion:
            
            # Check if chunk contains content.
            if chunk.choices[0].delta.content:
                
                # Append chunk to final response.
                answer += chunk.choices[0].delta.content



        # Remove unnecessary tokens.
        answer = answer.replace("</s>", "")



        # =================================================
        #             SAVE ASSISTANT RESPONSE
        # =================================================

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )



        # =================================================
        #              SAVE CHAT LOG FILE
        # =================================================

        with open(
            r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
            "w"
        ) as f:

            dump(messages, f, indent=4)



        # =================================================
        #             RETURN CLEAN RESPONSE
        # =================================================

        return AnswerModifier(answer)



    # =====================================================
    #                 ERROR HANDLING
    # =====================================================

    except Exception as e:
        # Print error.
        print("Error:", e)



        # ================================================
        #              RESET CHAT HISTORY
        # ================================================

        with open(
            r"C:\Users\hp\OneDrive\Desktop\jarvis_demo\Data\ChatLog.json",
            "w"
        ) as f:

            dump([], f)



        # Retry chatbot request.
        return ChatBot(query)



# =========================================================
#                   MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":

    # Infinite chatbot loop.
    while True:
        # Take user input.
        user_input = input("Enter Your Question: ")

        # Generate AI response.
        response = ChatBot(user_input)

        # Print response.
        print(response)