def getDrowsy(ret_1 , frame_1):
    import cv2
    import os
    from keras.models import load_model
    import numpy as np
    import pygame
    from pygame import mixer
    score=0


    mixer.init()
    sound = mixer.Sound(r"Alarm-Fast-High-Pitch-A1-www.fesliyanstudios.com.mp3")



    face = cv2.CascadeClassifier(".\haar cascade files\haarcascade_frontalface_alt.xml")
    leye = cv2.CascadeClassifier(".\haar cascade files\haarcascade_lefteye_2splits.xml")
    reye = cv2.CascadeClassifier(".\haar cascade files\haarcascade_righteye_2splits.xml")



    lbl=['Close','Open']

    model = load_model(".\models\cnnCat2.h5")
    path = os.getcwd()
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    count=0
    score=0
    thicc=2
    rpred=[99]
    lpred=[99]

    ret, frame = ret_1 , frame_1
    # height,width = frame.shape[:2] 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
    left_eye = leye.detectMultiScale(gray)
    right_eye =  reye.detectMultiScale(gray)

    #cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )

    # for (x,y,w,h) in faces:
    #     #cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

    for (x,y,w,h) in right_eye:
        r_eye=frame[y:y+h,x:x+w]
        count=count+1
        r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye,(24,24))
        r_eye= r_eye/255
        r_eye=  r_eye.reshape(24,24,-1)
        r_eye = np.expand_dims(r_eye,axis=0)
        #rpred = model.predict_step(r_eye)
        rpred = model.predict(r_eye)
        rpred=np.where(rpred[0][0] < 0.5, 0, 1)
        
        if(rpred==1):
            lbl='Open' 
        if(rpred==0):
            lbl='Closed'
        break

    for (x,y,w,h) in left_eye:
        l_eye=frame[y:y+h,x:x+w]
        count=count+1
        l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
        l_eye = cv2.resize(l_eye,(24,24))
        l_eye= l_eye/255
        l_eye=l_eye.reshape(24,24,-1)
        l_eye = np.expand_dims(l_eye,axis=0)
        lpred = model.predict(l_eye)#model.predict_classes(l_eye)
        lpred=np.where(lpred[0][0] < 0.5, 0, 1)
        
        if(lpred==1):
            lbl='Open'   
        if(lpred==0):
            lbl='Closed'
        break

    if(rpred==1 and lpred==1):
        score=1
        #cv2.putText(frame,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
    # if(rpred[0]==1 or lpred[0]==1):
    else:
        score=-3
        #cv2.putText(frame,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
    
    
    
    # if(score<0):
    #     score=0   
    # #cv2.putText(frame,'Score:'+str(score),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
    # if(score>40):
    #     #person is feeling sleepy so we beep the alarm
    #     #cv2.imwrite(os.path.join(path,'image.jpg'),frame)
    #     # try:
    #     if pygame.mixer.get_busy() == False:
    #             sound.play()
        
            
            #playsound(r'C:\Users\wwwyo\Downloads\archive (1)\Drowsiness detection\alarm.wav')
        # except :  # isplaying = False
        #     pass
    
        # if(thicc<16):
        #     thicc= thicc+2
        # else:
        #     thicc=thicc-2
        #     if(thicc<2):
        #         thicc=2
        # cv2.rectangle(frame,(0,0),(width,height),(0,0,255),thicc) 
        
    
    if score==40:
        try: 
            pygame.mixer.stop()
        except:
            pass
    return score
    #cv2.imshow('frame',frame)
    
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# cap.release()
# cv2.destroyAllWindows()