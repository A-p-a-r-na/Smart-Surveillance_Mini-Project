import cv2 
import time
import datetime 
import smtplib, ssl


def mail():

    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security   
    s.starttls()
    
    # Authentication  
    s.login("smartsurvelliancemini@gmail.com", "dprczumxpgyqgijj")
    
    
    # message to be sent   
    SUBJECT = "ALERT!!"   
    TEXT = "MOTION DETECTED"
    
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    cap = cv2.VideoCapture(0) #to set the camera
    #cap = cv2.VideoCapture('http://192.168.167.87:8080/video')

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml") 
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_fullbody_default.xml") 

    detection = False
    detection_stopped_time = None # to record a video for a certain period of time so that even if we leave the frame it will work for certain period of time
    timer_started = False # otherwise there will be many videos with millisec time 
    SECONDS_TO_RECORD_AFTER_DETECTION = 5






    frame_size = (int(cap.get(3)),int(cap.get(4))) #to record the video we need frame size
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") #to save the video in mp4

    while True :
        _,frame =cap.read() #to capture the first frame

        gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # frame to grayscale
        faces = face_cascade.detectMultiScale (gray, 1.3, 5)  # to detect face and to get them accurately lesser the num more accurate but take more time 
        bodies  = face_cascade.detectMultiScale (gray, 1.3, 5) # to detect body
        if len(faces)+ len (bodies)>0:
            if detection:     #if the body has already detected then don't stop continue to record ie detectinh previously
                timer_started =  False
            else:
                detection = True # if body has just detected
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") #to get the date and time for the recorded video
                out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
                font = cv2.FONT_HERSHEY_SIMPLEX
  
    # Use putText() method for
    # inserting text on video
                cv2.putText(frame, 'START RECORDING', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
                print("START RECORDING")
                # sending the mail    
                s.sendmail("smartsurvelliancemini@gmail.com", "aparnalekshmi23@gmail.com", message)
    
                # terminating the session    
                
        
        elif detection :
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started =False
                    out.release()
                    font = cv2.FONT_HERSHEY_SIMPLEX
  
    # Use putText() method for
    # inserting text on video
                    cv2.putText(frame, 'STOP RECORDING', (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)
                    print("STOP RECORDING")
                    

            else:       
                timer_started= True
                detection_stopped_time =time.time()
        if detection:

            out.write(frame)



    # for (x, y,width, height) in faces:
        #    cv2.rectangle(frame,(x,y),(x+width,y+height),(255,0,0), 3) #to draw rectangle on detected face 255 ,0,0 is bgr so blue line and 3 is the thickness

        cv2.imshow("Camera",frame) # title of window 

        if cv2.waitKey(1) == ord('q'):

            break                                                 # to break the loop
            

    out.release
    cap.release()
    cv2.destroyAllWindows()

