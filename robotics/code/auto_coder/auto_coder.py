"""
this code will scan hand written code, run it in the appropriate environment and run the expected test cases. the output of the code will be returned in a text file. 

code types:
1. arduino
2. python (comming soon)

# setup pip environment for MAC
python3 -m venv myenv 
source myenv/bin/activate
pip install pytesseract opencv-python 

# setup python libraries for raspberrypi
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng -y
sudo apt install libgl1-mesa-glx libglib2.0-0 -y
sudo apt install python3-opencv -y
"""

import os, cv2, numpy as np, pytesseract, time


def capture_image_from_video(camera_index: int = 1) -> np.array:
    # setup USB camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Camera index 1 not found. Attempting index 0...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("No USB camera detected.")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("Activating IPEVO Document Camera...")

    # focus and capture image
    start_time= time.time()
    while time.time() - start_time < 1.5:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Snapping Image...",cv2.resize(frame,(852,480)))
        cv2.waitKey(1)

    # Capture and finalize sharp, properly exposed frame
    ret, final_frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    if not ret or final_frame is None:
        raise RuntimeError("Failed to capture valid image from the camera feed.")

    return final_frame


def image_to_code(raw_image: np.ndarray) -> str: 
    """
    given an image, this will translate the image into text
    """
    # preprocess image with open cv
    if raw_image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")
    gray = cv2.cvtColor(raw_image,cv2. COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    sharpen_kernel = np.array([[-1,-1,-1],
                               [-1, 9,-1],
                               [-1,-1,-1]])
    sharpened = cv2.filter2D(denoised, -1, sharpen_kernel)
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("preprocessed_debug.png", thresh)

    # convert image to code
    custom_config = r'--oem 3 --psm 4'
    code_text = pytesseract.image_to_string(thresh, config=custom_config)

    return(code_text)


def upload_to_arduino(code_text):
    return(upload_outcome)


def serial_to_arduino(text_to_serial):
    """
    send text over serial and return the responce as text
    """
    return_text = ""
    return(return_text)


if __name__ == "__main__":
    # image to code
    raw_photo = capture_image_from_video(camera_index=1)
    code = image_to_code(raw_photo)
    print(code)
    # upload_responce = upload_to_arduino(image_to_code(read_image()))
    # test using arduino over serial
    # test_command = ""
    # arduino_response = serial_to_arduino(test_command)
