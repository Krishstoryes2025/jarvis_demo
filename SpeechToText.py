# =========================================================
#           JARVIS SPEECH RECOGNITION SYSTEM
# =========================================================
#
# Features:
#
# 1. Realtime Voice Recognition
# 2. Selenium Browser Automation
# 3. Automatic Language Translation
# 4. Query Formatting
# 5. Assistant Status Control
# 6. Live Speech Detection
# 7. Headless Chrome Automation
#
# =========================================================



# =========================================================
#                IMPORT REQUIRED LIBRARIES
# =========================================================

import subprocess



# =========================================================
#          INSTALL LIBRARIES IF NOT INSTALLED
# =========================================================

try:



    # Selenium browser automation.
    from selenium import webdriver



    # Locate HTML elements.
    from selenium.webdriver.common.by import By



    # Wait for webpage elements.
    from selenium.webdriver.support.ui import WebDriverWait



    # Selenium expected conditions.
    from selenium.webdriver.support import expected_conditions as EC



    # Chrome service controller.
    from selenium.webdriver.chrome.service import Service



    # Chrome browser options.
    from selenium.webdriver.chrome.options import Options



    # Automatically install ChromeDriver.
    from webdriver_manager.chrome import ChromeDriverManager



    # Current working directory.
    from os import getcwd



    # Language translator.
    import mtranslate as mt



# =========================================================
#            INSTALL MISSING MODULES AUTOMATICALLY
# =========================================================

except ModuleNotFoundError:



    # Install Selenium.
    subprocess.run(['pip', 'install', 'selenium'])



    # Install WebDriver Manager.
    subprocess.run(['pip', 'install', 'webdriver_manager'])



    # Install Translation Library.
    subprocess.run(['pip', 'install', 'mtranslate'])



    # Re-import after installation.
    from selenium import webdriver

    from selenium.webdriver.common.by import By

    from selenium.webdriver.support.ui import WebDriverWait

    from selenium.webdriver.support import expected_conditions as EC

    from selenium.webdriver.chrome.service import Service

    from selenium.webdriver.chrome.options import Options

    from webdriver_manager.chrome import ChromeDriverManager

    from os import getcwd

    import mtranslate as mt



# =========================================================
#              GET CURRENT DIRECTORY
# =========================================================

# Store current working directory.
current_dir = getcwd()



# =========================================================
#              CHROME BROWSER CONFIGURATION
# =========================================================

# Create Chrome options object.
chrome_options = Options()



# Automatically allow microphone access.
chrome_options.add_argument(
    "--use-fake-ui-for-media-stream"
)



# Run browser in background.
chrome_options.add_argument("--headless")



# =========================================================
#               CREATE CHROME DRIVER
# =========================================================

# Automatically install ChromeDriver.
service = Service(
    ChromeDriverManager().install()
)



# Launch Chrome browser.
driver = webdriver.Chrome(
    service=service,
    options=chrome_options
)



# =========================================================
#                   WEBSITE URL
# =========================================================

# Voice recognition website.
website = "https://allorizenproject1.netlify.app/"



# Open website.
driver.get(website)



# =========================================================
#              RECOGNIZED TEXT FILE
# =========================================================

# File to store recognized speech.
Recog_File = f"{getcwd()}\\Data\\input.txt"



# =========================================================
#               TEMPORARY DIRECTORY PATH
# =========================================================

# Path for assistant status files.
TempDirPath = rf"{current_dir}/Frontend/Files"



# =========================================================
#            ASSISTANT STATUS FUNCTION
# =========================================================

def SetAssistantStatus(Status):

    """
    Update assistant status.
    """



    # Open status file.
    with open(

        rf'{TempDirPath}/Status.data',

        "w",

        encoding='utf-8'

    ) as file:



        # Write current status.
        file.write(Status)



# =========================================================
#              QUERY MODIFICATION FUNCTION
# =========================================================

def QueryModifier(Query):

    """
    Clean and format user query.
    """



    # Convert to lowercase and remove spaces.
    new_query = Query.lower().strip()



    # Split query into words.
    query_words = new_query.split()



    # Question keywords.
    question_words = [

        "how",

        "what",

        "who",

        "where",

        "when",

        "why",

        "which",

        "whose",

        "whom",

        "can you",

        "what's",

        "wh"
    ]



    # =====================================================
    #              QUESTION DETECTION
    # =====================================================

    if any(word in new_query for word in question_words):



        # Add question mark.
        if query_words[-1][-1] in ['.', '?', '!']:



            new_query = new_query[:-1] + "?"



        else:

            new_query = new_query + "?"



    # =====================================================
    #               NORMAL STATEMENT
    # =====================================================

    else:



        # Add period.
        if query_words[-1][-1] in ['.', '?', '!']:



            new_query = new_query[:-1] + "."



        else:

            new_query = new_query + "."



    # Capitalize final sentence.
    return new_query.capitalize()



# =========================================================
#              UNIVERSAL TRANSLATOR
# =========================================================

def UniversalTranslator(Text):

    """
    Translate any language into English.
    """



    # Translate text.
    english_translation = mt.translate(

        Text,

        "en",

        "auto"
    )



    # Return translated text.
    return english_translation.capitalize()



# =========================================================
#                REALTIME LISTEN FUNCTION
# =========================================================

def listen():

    """
    Listen continuously using browser microphone.
    """

    try:



        # =================================================
        #            FIND START BUTTON
        # =================================================

        start_button = WebDriverWait(

            driver,

            20

        ).until(

            EC.element_to_be_clickable(
                (By.ID, 'startButton')
            )
        )



        # Start listening.
        start_button.click()



        print("Listening...")



        # Store recognized text.
        output_text = ""



        # Track listening state.
        is_second_click = False



        # =================================================
        #             CONTINUOUS LISTEN LOOP
        # =================================================

        while True:



            # Find output element.
            output_element = WebDriverWait(

                driver,

                10

            ).until(

                EC.presence_of_element_located(
                    (By.ID, 'output')
                )
            )



            # Get recognized text.
            current_text = output_element.text.strip()



            # =================================================
            #            CHECK LISTENING STATE
            # =================================================

            if (

                "Start Listening" in start_button.text

                and is_second_click
            ):



                if output_text:

                    is_second_click = False



            elif "Listening..." in start_button.text:

                is_second_click = True



            # =================================================
            #              DETECT TEXT CHANGES
            # =================================================

            if current_text != output_text:



                # Update stored text.
                output_text = current_text



                # Save recognized text.
                with open(

                    Recog_File,

                    "w"

                ) as file:



                    file.write(output_text.lower())



                    print("User:", output_text)



    # =====================================================
    #             HANDLE USER INTERRUPTION
    # =====================================================

    except KeyboardInterrupt:



        print("Process interrupted by user.")



    # =====================================================
    #                HANDLE ERRORS
    # =====================================================

    except Exception as e:



        print("An error occurred:", e)



    # =====================================================
    #              CLOSE BROWSER SAFELY
    # =====================================================

    finally:



        driver.quit()



# =========================================================
#            MAIN SPEECH RECOGNITION ENGINE
# =========================================================

def SpeechRecognition():

    """
    Convert speech into formatted text.
    """



    # Infinite listening loop.
    while True:

        try:



            # =================================================
            #              GET RECOGNIZED TEXT
            # =================================================

            Text = listen()



            # Skip empty input.
            if Text == "":

                continue



            # =================================================
            #               ENGLISH DETECTION
            # =================================================

            elif Text.isascii():



                # Return formatted English text.
                return QueryModifier(Text)



            # =================================================
            #            NON-ENGLISH TRANSLATION
            # =================================================

            else:



                # Translate to English.
                return QueryModifier(

                    UniversalTranslator(Text)
                )



        # =====================================================
        #                  HANDLE ERRORS
        # =====================================================

        except Exception:

            pass



# =========================================================
#                 MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":



    # Infinite assistant loop.
    while True:



        # =====================================================
        #             PERFORM SPEECH RECOGNITION
        # =====================================================

        Text = SpeechRecognition()

        # Print recognized query.
        print(Text)

        # Update assistant state.
        SetAssistantStatus("Listening")