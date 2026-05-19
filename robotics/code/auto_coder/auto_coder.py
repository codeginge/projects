"""
this code will scan hand written code, run it in the appropriate environment and run the expected test cases. the output of the code will be returned in a text file. 

code types:
1. arduino
2. python (comming soon)

# setup python libraries for raspberrypi
sudo apt update
sudo apt install libgl1-mesa-glx libglib2.0-0 -y
sudo apt install python3-opencv -y

# setup pip environment for MAC
python3 -m venv myenv
source myenv/bin/activate
pip install opencv-python==4.10.0.84
"""

import os, cv2, numpy as np, time, subprocess


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
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    time.sleep(0.1)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    print("Activating IPEVO Document Camera...")

    # focus and capture image
    start_time= time.time()
    while time.time() - start_time < 3.0:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Calibrating...",cv2.resize(frame,(852,480)))
        cv2.waitKey(1)

    # Capture and finalize sharp, properly exposed frame
    ret, final_frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    if not ret or final_frame is None:
        raise RuntimeError("Failed to capture valid image from the camera feed.")

    return final_frame


def image_to_code(raw_image: np.ndarray, black_white_threshold_line: int) -> str: 
    """
    given an image, this will translate the image into text
    """
    # preprocess image with open cv
    if raw_image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # crop image to page corners
    gray = cv2.cvtColor(raw_image,cv2. COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh_corners = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh_corners, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    page_corners = None
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            page_corners = approx
            break

    if page_corners is not None:
        pts = page_corners.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(widthA), int(widthB))
        
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(heightA), int(heightB))
        
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")
        
        M = cv2.getPerspectiveTransform(rect, dst)
        cropped_image = cv2.warpPerspective(raw_image, M, (max_width, max_height))
        cv2.imwrite("cropped_image.png", cropped_image)
    else:
        cropped_image = raw_image.copy()  # Fallback to original if no 4-point page is detected

    # convert cropped image to black and white
    gray_cropped = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)    
    denoised = cv2.bilateralFilter(gray_cropped, d=9, sigmaColor=75, sigmaSpace=75)
    sharpen_kernel = np.array([[-1,-1,-1],
                               [-1, 9,-1],
                               [-1,-1,-1]])
    sharpened = cv2.filter2D(denoised, -1, sharpen_kernel)
    _, thresh = cv2.threshold(sharpened, black_white_threshold_line, 255, cv2.THRESH_BINARY)
    cv2.imwrite("preprocessed_debug.png", thresh)

    # convert image to code
    ocr_ready_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    temp_img_path = "processed_image.png"
    cv2.imwrite(temp_img_path, thresh)

    prompt = (
        "You are a strict code extraction tool. Look at this handwritten text "
        "and output ONLY valid, executable Arduino C++ code. Do not include markdown code blocks, "
        "do not explain anything, do not add pleasantries. Just the code."
    )
    cmd = [
        "./llama.cpp/build/bin/llama-cli",
        "-m", "./models/Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf",
        "--mmproj", "./models/mmproj-Qwen2.5-VL-3B-Instruct-Q4_K_M.gguf",
        "--image", temp_img_path,
        # System flag to strictly dictate behavioral output constraints
        "-sys", "You are a strict code extraction tool. Look at this handwritten text and output ONLY valid, executable Arduino C++ code. Do not include markdown code blocks, explanations, or pleasantries.",
        # Prompt flag tells the model what to do with the specific image
        "-p", "Transcribe the code from this image.",
        "-n", "512", # Maximum token threshold for the generated response
        "-c", "3072", # Expanded safely to account for visual patch tokens + your 512 output
        "-t", "4" # Parallelizes across exactly 4 processing cores
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("\n[ERROR] llama.cpp execution failed!")
        print("--- Diagnostic System Error Output ---")
        print(result.stderr)  # This will print the exact issue (e.g., file not found, bad path)
        print("---------------------------------------")
        raise RuntimeError(f"Subprocess failed with exit code {result.returncode}")

    raw_output = result.stdout.strip()
    code_text = raw_output.replace("```cpp", "").replace("```", "").strip()
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

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
    bw_thresh = 200
    raw_photo = capture_image_from_video(camera_index=1)
    code = image_to_code(raw_photo, bw_thresh)
    print(code)
    # upload_responce = upload_to_arduino(image_to_code(read_image()))
    # test using arduino over serial
    # test_command = ""
    # arduino_response = serial_to_arduino(test_command)
