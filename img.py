import datetime
import requests
import streamlit as st

# Function to upload an image to ImgBB and get the direct link
def upload_image_to_imgbb(image, api_key):
    try:
        # Upload the image to ImgBB using the API
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": api_key},
            files={"image": image},
        )

        # Parse the JSON response
        result = response.json()

        if "data" in result and "url" in result["data"]:
            # Return the direct link to the uploaded image
            return result["data"]["url"]
        else:
            return None

    except Exception as e:
        return str(e)

st.title("Image Upload and WhatsApp Message")

source_img = st.sidebar.file_uploader(
    "Choose an image...", type=("jpg", "jpeg", "png", "bmp", "webp"))

if source_img is not None:
    st.write("Image Uploaded:")
    st.image(source_img, use_column_width=True)

    imgbb_api_key = "YOUR_API_KEY_HERE"  # Replace with your ImgBB API key

    try:
        image_link = upload_image_to_imgbb(source_img.read(), imgbb_api_key)  # Use .read() to get the file data
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute

        # Display the image link as text
        st.write("Image Link:")
        st.text(image_link)

        # Replace with your WhatsApp message sending code here
        # kit.sendwhatmsg("+919398058458", "garbage detection " + image_link, current_hour, current_minute + 1)

    except Exception as ex:
        st.error
