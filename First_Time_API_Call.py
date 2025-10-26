from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

# --- Configuration ---
INPUT_IMAGE_PATH = 'Jua.jpg'
EDIT_PROMPT = "Make this look like dali art."
OUTPUT_FILENAME = "Juan_after.jpg"
MODEL = "gemini-2.5-flash-image" # Use the image generation model

# --- Client Initialization ---
client = genai.Client()

# --- Step 1: Upload the Image using the Files API ---
try:
    print(f"⬆️ Uploading image '{INPUT_IMAGE_PATH}'...")
    # The Files API is best for images used in generation/editing tasks
    uploaded_file = client.files.upload(file=INPUT_IMAGE_PATH)
    print(f"   Image uploaded. File URI: {uploaded_file.uri}")

except FileNotFoundError:
    print(f"❌ ERROR: Input image '{INPUT_IMAGE_PATH}' not found.")
    exit()
except Exception as e:
    print(f"❌ ERROR during file upload: {e}")
    exit()

# --- Step 2: Send Multimodal Prompt for Editing ---
try:
    print(f"🎨 Requesting edit based on prompt: '{EDIT_PROMPT[:50]}...'")
    
    response = client.models.generate_content(
        model=MODEL,
        # Contents list contains both the text prompt and the uploaded file reference
        contents=[EDIT_PROMPT, uploaded_file],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

except Exception as e:
    print(f"❌ API Call Failed: {e}")
    client.files.delete(name=uploaded_file.name) # Clean up on failure
    exit()

# --- Step 3: Process the New Image Output and Clean Up ---
image_found = False
for part in response.parts:
    if part.inline_data:
        image_bytes = part.inline_data.data
        
        # Decode and save the new image
        generated_image = Image.open(BytesIO(image_bytes))
        generated_image.save(OUTPUT_FILENAME)
        
        print(f"\n✅ New image successfully generated and saved to: {OUTPUT_FILENAME}")
        image_found = True
        
    elif part.text:
        print(f"✍️ Model Commentary: {part.text}")

if not image_found:
    print("❌ Image data was not found in the response.")

# --- Final Step: Clean Up the Uploaded File ---
client.files.delete(name=uploaded_file.name)
print(f"🧹 Clean up complete. Deleted uploaded file: {uploaded_file.name}")