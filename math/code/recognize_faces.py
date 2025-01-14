import cv2
import os
import face_recognition

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to load images from a directory
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            images.append(face_recognition.load_image_file(img_path))
    return images

# Function to recognize faces in the frame
def recognize_faces(frame, known_faces_encodings, known_names, font_scale):
    # Find face locations
    face_locations = face_recognition.face_locations(frame)
    # Find face encodings
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare the face with known faces
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, use the name of the known face
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        # Draw a rectangle and put text with the name on the frame
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 6), cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 255, 255), 1)

    return frame

# Directory containing images of known people
known_people_folder = 'known_people'

# Load images and their encodings from the directory
known_face_images = []
known_faces_encodings = []
known_names = []

people_list=[]

for person_name in os.listdir(known_people_folder):
    person_folder = os.path.join(known_people_folder, person_name)
    if os.path.isdir(person_folder):
        person_images = load_images_from_folder(person_folder)
        for image in person_images:
            try:
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_images.append(image)
                known_faces_encodings.append(face_encoding)
                known_names.append(person_name)
            except IndexError:
                print(f"Face encoding not found for {os.path.basename(image)}")

# Open the default camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = recognize_faces(frame, known_faces_encodings, known_names, 1)
    cv2.imshow('Face Recognition', frame)

    clear_screen
    print(known_names)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
