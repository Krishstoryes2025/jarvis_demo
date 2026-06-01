# =========================================================
#         JARVIS HYBRID ONLINE + OFFLINE TTS SYSTEM
# =========================================================
#
# Features:
#
# 1. Online Edge-TTS Voice (High Quality)
# 2. Automatic Offline Fallback
# 3. Works Without Internet
# 4. JARVIS-like Voice
# 5. Error Recovery
# 6. Fast Playback
# 7. Smart Long Response Handling
#
# =========================================================



# =========================================================
#                IMPORT REQUIRED LIBRARIES
# =========================================================

import pygame
import random
import asyncio
import edge_tts
import os
import pyttsx3

from dotenv import dotenv_values



# =========================================================
#              LOAD ENVIRONMENT VARIABLES
# =========================================================

env_vars = dotenv_values(".env")



# Online AI voice.
AssistantVoice = env_vars.get(
    "AssistantVoice",
    "en-US-AndrewNeural"
)



# =========================================================
#              INITIALIZE OFFLINE TTS ENGINE
# =========================================================

# pyttsx3 works completely offline.
engine = pyttsx3.init()



# =========================================================
#           CONFIGURE OFFLINE VOICE SETTINGS
# =========================================================

voices = engine.getProperty("voices")



# Select male voice if available.
for voice in voices:

    if "male" in voice.name.lower():

        engine.setProperty("voice", voice.id)

        break



# Voice speed.
engine.setProperty("rate", 185)



# Voice volume.
engine.setProperty("volume", 1.0)



# =========================================================
#             ONLINE EDGE-TTS GENERATION
# =========================================================

async def TextToAudioFile(Text) -> None:

    """
    Generate AI speech using Edge-TTS.
    """



    file_path = r"Data\speech.mp3"



    # Delete old file.
    if os.path.exists(file_path):

        os.remove(file_path)



    # Create Edge-TTS request.
    communicate = edge_tts.Communicate(

        Text,

        AssistantVoice,

        pitch="+5Hz",

        rate="+13%"
    )



    # Save generated audio.
    await communicate.save(file_path)



# =========================================================
#               OFFLINE FALLBACK TTS
# =========================================================

def OfflineTTS(Text):

    """
    Offline speech system using pyttsx3.
    """



    print("[Offline TTS Activated]")



    engine.say(Text)

    engine.runAndWait()



# =========================================================
#                MAIN TTS PLAYBACK
# =========================================================

def TTS(Text, func=lambda r=None: True):

    """
    Main speech playback engine.
    """



    while True:

        try:



            # =================================================
            #         TRY ONLINE EDGE-TTS FIRST
            # =================================================

            asyncio.run(TextToAudioFile(Text))



            # =================================================
            #              PLAY GENERATED AUDIO
            # =================================================

            pygame.mixer.init()



            pygame.mixer.music.load(
                r"Data\speech.mp3"
            )



            pygame.mixer.music.play()



            # =================================================
            #          WAIT UNTIL AUDIO FINISHES
            # =================================================

            while pygame.mixer.music.get_busy():



                if func() == False:

                    break



                pygame.time.Clock().tick(10)



            return True



        # =====================================================
        #          IF ONLINE TTS FAILS -> OFFLINE TTS
        # =====================================================

        except Exception as e:



            print(
                "\n[Online TTS Failed]"
            )



            print(
                "Reason:",
                e
            )



            print(
                "Switching To Offline Voice...\n"
            )



            # =================================================
            #            USE OFFLINE SPEECH
            # =================================================

            OfflineTTS(Text)



            return True



        # =====================================================
        #                CLEANUP OPERATIONS
        # =====================================================

        finally:

            try:



                func(False)



                pygame.mixer.music.stop()



                pygame.mixer.quit()



            except:

                pass



# =========================================================
#             SMART TEXT TO SPEECH FUNCTION
# =========================================================

def TextToSpeech(Text, func=lambda r=None: True):

    """
    Smart speech system for long responses.
    """



    # Split text into sentences.
    Data = str(Text).split(".")



    # =====================================================
    #        SHORT RESPONSE MESSAGES
    # =====================================================

    responses = [

        "The rest of the result has been printed to the chat screen, kindly check it out sir.",

        "The rest of the text is now on the chat screen, sir.",

        "You can see the rest of the text on the chat screen, sir.",

        "Sir, please check the chat screen for more information.",

        "The complete answer is available on the chat screen, sir.",

        "Sir, kindly review the remaining text on the display screen."
    ]



    # =====================================================
    #              HANDLE LONG RESPONSES
    # =====================================================

    if len(Data) > 4 and len(Text) >= 250:



        ShortText = (

            "".join(Text.split(".")[0:2])

            + ". "

            + random.choice(responses)
        )



        TTS(ShortText, func)



    # =====================================================
    #               NORMAL RESPONSE
    # =====================================================

    else:



        TTS(Text, func)



# =========================================================
#                  MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":



    while True:



        user_input = input(
            "\nEnter text to convert to speech:\n>>> "
        )



        TextToSpeech(user_input)