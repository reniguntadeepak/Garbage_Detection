import datetime
import pywhatkit as pwk
import requests
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

image_path = "detection module.png"
imgbb_api_key = "19d5ace2a00725cbb013271137f0a3ed"

try:
    image_link = upload_image_to_imgbb(image_path, imgbb_api_key)
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    pwk.sendwhatmsg("+919398058458", "garbage detection "+image_link,current_hour,current_minute+1)
    print("Message Sent!")
except Exception as ex:     
    print(ex)