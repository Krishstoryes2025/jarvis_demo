import asyncio
from random import randint
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from time import sleep
import os


# -----------------------------------------
# Load .env variables
# -----------------------------------------
load_dotenv()

# Get Hugging Face API key
API_KEY = os.getenv("HuggingFaceAPIKey")

# Create Hugging Face client
client = InferenceClient(api_key=API_KEY)


# -----------------------------------------
# Create Data folder if missing
# -----------------------------------------
os.makedirs("Data", exist_ok=True)


# -----------------------------------------
# Open generated images
# -----------------------------------------
def open_images(prompt):

    folder_path = "Data"

    # Replace spaces with underscore
    prompt = prompt.replace(" ", "_")

    # Create file list
    files = [f"{prompt}{i}.png" for i in range(1, 5)]

    for image_file in files:

        image_path = os.path.join(
            folder_path,
            image_file
        )

        try:

            img = Image.open(image_path)

            print(
                f"Opening image: {image_path}"
            )

            img.show()

            sleep(1)

        except Exception as e:

            print(
                f"Unable to open {image_path}"
            )

            print(e)


# -----------------------------------------
# Generate single image
# -----------------------------------------
async def query(prompt, index):

    try:

        image = await asyncio.to_thread(

            client.text_to_image,

            prompt=(
                f"{prompt}, "
                f"quality=4k, "
                f"Ultra High details, "
                f"high resolution, "
                f"seed={randint(0,1000000)}"
            ),

            model="black-forest-labs/FLUX.1-schnell"
        )

        filename = os.path.join(
            "Data",
            f"{prompt.replace(' ','_')}{index}.png"
        )

        image.save(filename)

        print(
            f"Saved: {filename}"
        )

        return True

    except Exception as e:

        print(
            "Generation Error:",
            e
        )

        return False


# -----------------------------------------
# Generate multiple images
# -----------------------------------------
async def generate_image(prompt: str):

    tasks = []

    # Create 4 image generation tasks
    for i in range(1, 5):

        task = asyncio.create_task(
            query(prompt, i)
        )

        tasks.append(task)

    results = await asyncio.gather(
        *tasks
    )

    return any(results)


# -----------------------------------------
# Main generation function
# -----------------------------------------
def GenerateImages(prompt: str):

    success = asyncio.run(
        generate_image(prompt)
    )

    # Open images only if generated
    if success:

        open_images(prompt)

    else:

        print(
            "No images generated"
        )


# -----------------------------------------
# Continuous monitoring loop
# -----------------------------------------
while True:

    try:

        print(
            "Checking file..."
        )

        with open(
            r"Frontend\Files\ImageGeneration.data",
            "r"
        ) as f:

            Data = f.read().strip()

        Prompt, Status = Data.split(",")

        print(
            "Prompt:",
            Prompt
        )

        print(
            "Status:",
            Status
        )

        if Status.strip() == "True":

            print(
                "Generating images..."
            )

            GenerateImages(
                prompt=Prompt
            )

            # Reset status after generation
            with open(
                r"Frontend\Files\ImageGeneration.data",
                "w"
            ) as f:

                f.write(
                    "False,False"
                )

        else:

            sleep(2)

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        sleep(2)