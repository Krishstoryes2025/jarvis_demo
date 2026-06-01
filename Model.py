# =========================================================
#              JARVIS DECISION MAKING MODEL
# =========================================================
#
# Features:
#
# 1. Query Classification
# 2. Automation Detection
# 3. Multi-Command Parsing
# 4. Real-Time Query Detection
# 5. App Control Command Detection
# 6. Content Generation Detection
# 7. Reminder Detection
# 8. YouTube & Google Search Detection
#
# =========================================================



# =========================================================
#                IMPORT REQUIRED LIBRARIES
# =========================================================

# Cohere AI library.
import cohere

# Rich library for styled terminal printing.
from rich import print

# Load environment variables from .env file.
from dotenv import dotenv_values



# =========================================================
#              LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load variables from .env file.
env_vars = dotenv_values(
    "C:\\Users\\hp\\OneDrive\\Desktop\\jarvis_demo\\.env"
)

# Retrieve Cohere API key.
CohereAPIKey = env_vars.get("CohereAPIKey")



# =========================================================
#               INITIALIZE COHERE CLIENT
# =========================================================

# Create Cohere AI client.
co = cohere.Client(api_key=CohereAPIKey)



# =========================================================
#             LIST OF SUPPORTED FUNCTIONS
# =========================================================

# These are all recognized command categories.
funcs = [

    "exit",

    "general",

    "realtime",

    "open",

    "close",

    "play",

    "generate image",

    "system",

    "content",

    "google search",

    "youtube search",

    "reminder"
]



# =========================================================
#               CONVERSATION MEMORY
# =========================================================

# Stores temporary messages.
messages = []



# =========================================================
#                 SYSTEM PREAMBLE
# =========================================================

# This preamble trains the model
# to behave as a decision-making engine.
preamble = """

You are a very accurate Decision-Making Model,
which decides what kind of query is given to you.

You will decide whether a query is:

1. General Query
2. Realtime Query
3. Automation Task

*** Do not answer any query. ***
*** Only classify the query. ***



# =====================================================
#                  GENERAL QUERY
# =====================================================

Respond with:

general (query)

if the query:

- can be answered by a normal AI chatbot
- does not need realtime information
- is conversational
- is educational
- is incomplete



# =====================================================
#                  REALTIME QUERY
# =====================================================

Respond with:

realtime (query)

if the query:

- needs current information
- requires latest news
- asks about current people/events
- asks today's updates



# =====================================================
#                   OPEN COMMAND
# =====================================================

Respond with:

open (app name)

if user wants to open apps/websites.



# =====================================================
#                   CLOSE COMMAND
# =====================================================

Respond with:

close (app name)

if user wants to close applications.



# =====================================================
#                    PLAY COMMAND
# =====================================================

Respond with:

play (song name)

if user wants to play songs/videos.



# =====================================================
#               GENERATE IMAGE COMMAND
# =====================================================

Respond with:

generate image (prompt)

if user wants image generation.



# =====================================================
#                  REMINDER COMMAND
# =====================================================

Respond with:

reminder (datetime + message)

if user wants reminders.



# =====================================================
#                  SYSTEM COMMAND
# =====================================================

Respond with:

system (task)

for:
- mute
- unmute
- volume up
- volume down



# =====================================================
#                  CONTENT COMMAND
# =====================================================

Respond with:

content (topic)

if user wants:
- code
- email
- application
- article
- letter
- script
- anything written



# =====================================================
#               GOOGLE SEARCH COMMAND
# =====================================================

Respond with:

google search (topic)

if user wants Google search.



# =====================================================
#              YOUTUBE SEARCH COMMAND
# =====================================================

Respond with:

youtube search (topic)

if user wants YouTube search.



# =====================================================
#                  MULTIPLE TASKS
# =====================================================

If multiple commands exist:

Example:

open chrome, close whatsapp



# =====================================================
#                  EXIT COMMAND
# =====================================================

If user says goodbye:

respond with:

exit



# =====================================================
#                FALLBACK CONDITION
# =====================================================

If unsure:

respond with:

general (query)

"""


# =========================================================
#                 FEW-SHOT TRAINING
# =========================================================

# These examples help the model learn
# the expected response format.
ChatHistory = [

    {
        "role": "User",
        "message": "how are you?"
    },

    {
        "role": "Chatbot",
        "message": "general how are you?"
    },



    {
        "role": "User",
        "message": "do you like pizza?"
    },

    {
        "role": "Chatbot",
        "message": "general do you like pizza?"
    },



    {
        "role": "User",
        "message": "open chrome and tell me about mahatma gandhi."
    },

    {
        "role": "Chatbot",
        "message": "open chrome, general tell me about mahatma gandhi."
    },



    {
        "role": "User",
        "message": "open chrome and firefox"
    },

    {
        "role": "Chatbot",
        "message": "open chrome, open firefox"
    },



    {
        "role": "User",
        "message": "what is today's date and remind me about meeting at 11pm"
    },

    {
        "role": "Chatbot",
        "message": "general what is today's date, reminder 11pm meeting"
    },



    {
        "role": "User",
        "message": "chat with me"
    },

    {
        "role": "Chatbot",
        "message": "general chat with me"
    }
]



# =========================================================
#              MAIN DECISION-MAKING FUNCTION
# =========================================================

def FirstLayerDMM(prompt: str = "test"):

    """
    First Layer Decision Making Model.

    This function classifies user queries
    into executable command categories.
    """



    # =====================================================
    #                STORE USER QUERY
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": f"{prompt}"
        }
    )



    # =====================================================
    #              CREATE STREAMING SESSION
    # =====================================================

    stream = co.chat_stream(

        # Cohere model name.
        model='command-a-03-2025',

        # User input.
        message=prompt,

        # Creativity level.
        temperature=0.7,

        # Previous examples.
        chat_history=ChatHistory,

        # Prevent truncation.
        prompt_truncation='OFF',

        # No external connectors.
        connectors=[],

        # System instructions.
        preamble=preamble
    )

    # =====================================================
    #               STORE GENERATED RESPONSE
    # =====================================================

    response = ""


    # =====================================================
    #             RECEIVE STREAMED RESPONSE
    # =====================================================

    for event in stream:

        # Check text generation event.
        if event.event_type == "text-generation":

            # Append generated text.
            response += event.text

    # =====================================================
    #                 CLEAN RESPONSE
    # =====================================================

    # Remove newline characters.
    response = response.replace("\n", "")

    # Split multiple commands.
    response = response.split(",")

    # Remove unnecessary spaces.
    response = [i.strip() for i in response]


    # =====================================================
    #               FILTER VALID TASKS
    # =====================================================

    temp = []


    # Check every generated task.
    for task in response:

        # Match supported commands.
        for func in funcs:

            # Check if task starts with valid function.
            if task.startswith(func):

                # Store valid task.
                temp.append(task)

    # Update response.
    response = temp


    # =====================================================
    #                RECURSION SAFETY
    # =====================================================

    # Retry if model returns invalid placeholder.
    if "(query)" in str(response):
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse

    # =====================================================
    #                  RETURN TASKS
    # =====================================================

    else:
        return response



# =========================================================
#                  MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":

    # Infinite loop.
    while True:

        # Take user input.
        user_input = input(">>>: ")
        
        # Process user query.
        result = FirstLayerDMM(user_input)

        # Print classified tasks.
        print(result)