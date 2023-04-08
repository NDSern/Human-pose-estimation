import cv2
import mediapipe as mp
import numpy as np
import time
import json

# Drawing tools for video capturing
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Start video capturing
cap = cv2.VideoCapture(r'D:\LMAO\temp\gif\test.gif')

# List of landmark for sending
landmarksList = []

# Python Dictionary of Landmarks
landmarkDict = []

# FPS or tick per sec
fps = 0

# Print to console 
def print_landmarks(landmarks):
    i = 0
    for point in landmarks:
        # print(point, ". ", landmarks[point].x, "/",  landmarks[point].y, "/", landmarks[point].z)
        print(i, ". ", str(point.x)[:8], "/",
              str(point.y)[:8], "/", str(point.z)[:8])
        i += 1
    print(len(landmarksList))
    print("------------------------------")

# Reformat landmark list
def landmarks_list(landmarks):
    for point in landmarks:
        # take 6 decimal
        a = str(point.x)[:8]
        b = str(point.y)[:8]
        c = str(point.z)[:8]
        newLine = f'{a},{b},{c},'
        landmarksList.append(newLine)
        #manually counting frames
        #print(len(landmarksList)/33)
        
# Reformat landmark list
def add_line(frames, joint, a, b, c):
    # take 6 decimal
    a = str(a)[:8]
    b = str(b)[:8]
    c = str(c)[:8]
    newLine = f'{a},{b},{c},'
    landmarksList.append(newLine)
    
    node = {
        "name" : joint,
        "position": {
            "x": a,
            "y": b,
            "z": c
        },
        "scale": {
            "x": 1.0,
            "y": 1.0,
            "z": 1.0
        }
    }
    landmarkDict[frames]["bones"].append(node)
    
# Reformat landmark list to the other thingy
def modified_landmarks_list(landmarks, frames):
    # Counting frames
    landmarkDict.append({
        "times" : frames + 1,
        "bones" : []
    })
    frames = frames + 1
    
    for i in range(52):
        match i:
            case 0:
                joint = "Hips"
                a = (landmarks[23].x + landmarks[24].x) / 2
                b = (landmarks[23].y + landmarks[24].y) / 2
                c = (landmarks[23].z + landmarks[24].z) / 2
                add_line(frames, joint, a, b, c)
            case 4:
                joint = "Neck"
                a = (landmarks[11].x + landmarks[12].x) / 2
                b = (landmarks[11].y + landmarks[12].y) / 2
                c = (landmarks[11].z + landmarks[12].z) / 2
                add_line(frames, joint, a, b, c)
            case 5:
                joint = "Head"
                a = landmarks[0].x
                b = landmarks[0].y
                c = landmarks[0].z
                add_line(frames, joint, a, b, c)
            case 7:
                joint = "LeftArm"
                a = landmarks[11].x
                b = landmarks[11].y
                c = landmarks[11].z
                add_line(frames, joint, a, b, c)
            case 8:
                joint = "LeftForeArm"
                a = landmarks[13].x
                b = landmarks[13].y
                c = landmarks[13].z
                add_line(frames, joint, a, b, c)
            case 9:
                joint = "LeftHand"
                a = landmarks[15].x
                b = landmarks[15].y
                c = landmarks[15].z
                add_line(frames, joint, a, b, c)
            case 10:
                joint = "LeftHandThumb1"
                a = landmarks[21].x
                b = landmarks[21].y
                c = landmarks[21].z
                add_line(frames, joint, a, b, c)
            case 26:
                joint = "RightArm"
                a = landmarks[12].x
                b = landmarks[12].y
                c = landmarks[12].z
                add_line(frames, joint, a, b, c)
            case 27:
                joint = "RightForeArm"
                a = landmarks[14].x
                b = landmarks[14].y
                c = landmarks[14].z
                add_line(frames, joint, a, b, c)
            case 28:
                joint = "RightHand"
                a = landmarks[16].x
                b = landmarks[16].y
                c = landmarks[16].z
                add_line(frames, joint, a, b, c)
            case 29:
                joint = "RightHandThumb1"
                a = landmarks[22].x
                b = landmarks[22].y
                c = landmarks[22].z
                add_line(frames, joint, a, b, c)
            case 44:
                joint = "LeftUpLeg"
                a = landmarks[23].x
                b = landmarks[23].y
                c = landmarks[23].z
                add_line(frames, joint, a, b, c)
            case 45:
                joint = "LeftLeg"
                a = landmarks[25].x
                b = landmarks[25].y
                c = landmarks[25].z
                add_line(frames, joint, a, b, c)
            case 46:
                joint = "LeftFoot"
                a = landmarks[27].x
                b = landmarks[27].y
                c = landmarks[27].z
                add_line(frames, joint, a, b, c)
            case 47:
                joint = "LeftToeBase"
                a = landmarks[31].x
                b = landmarks[31].y
                c = landmarks[31].z
                add_line(frames, joint, a, b, c)
            case 48:
                joint = "RightUpLeg"
                a = landmarks[24].x
                b = landmarks[24].y
                c = landmarks[24].z
                add_line(frames, joint, a, b, c)
            case 49:
                joint = "RightLeg"
                a = landmarks[26].x
                b = landmarks[26].y
                c = landmarks[26].z
                add_line(frames, joint, a, b, c)
            case 50:
                joint = "RightFoot"
                a = landmarks[28].x
                b = landmarks[28].y
                c = landmarks[28].z
                add_line(frames, joint, a, b, c)
            case 51:
                joint = "RightToeBase"
                a = landmarks[32].x
                b = landmarks[32].y
                c = landmarks[32].z
                add_line(frames, joint, a, b, c)

if __name__ == "__main__":
    # Pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, static_image_mode=1) as pose:
        frames = 0
        while cap.isOpened():            
            ret, frame = cap.read()
            
            # close the vid
            if not ret:
                print("No more frame")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)           

            # ok now try extract everything, there is a list of 0->32
            try:
                landmarks = results.pose_landmarks.landmark
                #print_landmarks(landmarks)
                #landmarks_list(landmarks)
                modified_landmarks_list(landmarks, frames)
                frames = frames + 1
                #time.sleep(0.1)
            except:
                pass

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Cap", image)
                        
            # Save points to new files
            if cv2.waitKey(21) & 0xFF == ord('q'):
                break
            
        #FPS or tick per second for animation
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        
        with open("./formatted.txt", 'w') as f:
            f.writelines(["%s\n" % item for item in landmarksList])
        with open("./string.txt", 'w') as f:
            f.writelines([item for item in landmarksList])
                
    
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    
    #Dimension
    width = cap.get(3)
    height = cap.get(4)    
    
    #Json
    landmarkDict.pop(0)
    dataDict = {
        "duration" : frames, 
        "width" : width,
        "height" : height,
        "ticksPerSecond" : fps,
        "frames" : landmarkDict
    }
    
    
    dataJson = json.dumps(dataDict)    
    with open('output.json', 'w') as json_file:
        json.dump(dataDict, json_file, indent=4, )
        
    cap.release()
    cv2.destroyAllWindows()
