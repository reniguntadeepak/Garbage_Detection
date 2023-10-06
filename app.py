# Python In-built packages
from pathlib import Path
import PIL
import pywhatkit as kit
import datetime
import requests
# External packages
import streamlit as st

# Local Modules
import settings
import helper
length=0
# Setting page layout
st.set_page_config(
    page_title="Object Detection using YOLOv8",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Garbage Detection using YOLOv8")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                length=len(res[0].boxes.cls)
                st.write('Garbage Detected:',length)
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)

                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")


def upload_image_to_imgbb(image_path, api_key):
    try:
        # Upload the image to ImgBB using the API
        with open(image_path, "rb") as file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={"key": api_key},
                files={"image": file},
            )

            # Parse the JSON response
            result = response.json()

            if "data" in result and "url" in result["data"]:
                # Return the direct link to the uploaded image
                return result["data"]["url"]
            else:
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
# print(source_img.name)
# print(source_img)
# image_path = source_img.read()
imgbb_api_key = "19d5ace2a00725cbb013271137f0a3ed"
if length >= 1:  # Adjust the condition as needed
    try:
        # image_link = upload_image_to_imgbb(image_path, imgbb_api_key)
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        kit.sendwhatmsg("+917013545123", "Hey, Grbage detected in street no 1 BK enclave, Clean it as soon as possible ",current_hour,current_minute+1)
        print("Message Sent!")
    except Exception as ex:     
        print(ex)