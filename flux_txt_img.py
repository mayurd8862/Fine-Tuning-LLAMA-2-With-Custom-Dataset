import streamlit as st
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()
# Access the token
token = os.getenv('HF_TOKEN')

# API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
# API_URL = "https://api-inference.huggingface.co/models/ByteDance/Hyper-SD"
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {token}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Error: " + str(response.status_code) + " " + response.text)
        return None

st.title("Image Generator")
st.write("Generate an image using a text prompt.")

# Text input for user
prompt = st.text_input("Enter a description:", "cute girl smiling")

if st.button("Generate Image"):
    image_bytes = query({"inputs": prompt})
    if image_bytes:
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Generated Image", use_column_width=True)
        
        # Save the image to a local directory
        save_path = "generated_image.png"
        image.save(save_path)
        st.success(f"Image saved as {save_path}")

        # Provide download link
        with open(save_path, "rb") as file:
            st.download_button(
                label="Download Image",
                data=file,
                file_name=save_path,
                mime="image/png"
            )
