import cv2  # import cv
import numpy as np
import time
import numpy as np
from tkinter import *
import tkinter.messagebox
import os
import tensorflow 
from pygame import mixer
from playsound import playsound
from PIL import Image, ImageDraw
import face_recognition
from tensorflow import keras
from imutils.video import FPS
import smtplib
import telegram
import config
from os import environ
from twilio.rest import Client

root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('DDDS')
frame.config(background='light blue')
label = Label(frame, text="DDD System",bg='light blue',font=('Times 35 bold'))
labell =Label(frame, text="Registration Form",bg='light blue',font=('Times 35 bold'))
label.pack(side=TOP)
filename = PhotoImage(file="2019-web-DP-AI.png")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)

def hel():
   help(cv2)

def Contri():
   tkinter.messagebox.showinfo("Contributors","\n1.Abenezer Berhanu\n2. Kaleb Tesfaye \n3. Sofonias Simon \n")


def anotherWin():
   tkinter.messagebox.showinfo("About",'Driver Detection and Alerting System v1.0\n Made Using\n-Convolutional Neural Network(CNN)\n-Tensorflow-Keras\n-Opencv\n In Python 3')
                                    
   

menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools",menu=subm1)
subm1.add_command(label="Open CV Docs",command=hel)

subm2 = Menu(menu)
menu.add_cascade(label="About",menu=subm2)
subm2.add_command(label="DDD",command=anotherWin)
subm2.add_command(label="Contributors",command=Contri)

def exitt():
   exit()

  
def web():
   capture =cv2.VideoCapture(0)
   while True:
      ret,frame=capture.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF ==ord('q'):
         break
   capture.release()
   cv2.destroyAllWindows()
  




# set a counter
counter = 0

eye_model = keras.models.load_model('driverDrowsymodelIncep.h5')

def eye_cropper(frame):

    # create a variable for the facial feature coordinates
    facial_features_list = face_recognition.face_landmarks(frame)

    # create a placeholder list for the eye coordinates
    # and append coordinates for eyes to list unless eyes
    # weren't found by facial recognition
    try:
        eye = facial_features_list[0]['left_eye']
    except:
        try:
            eye = facial_features_list[0]['right_eye']
        except:
            return

    # establish the max x and y coordinates of the eye
    x_max = max([coordinate[0] for coordinate in eye])
    x_min = min([coordinate[0] for coordinate in eye])
    y_max = max([coordinate[1] for coordinate in eye])
    y_min = min([coordinate[1] for coordinate in eye])

    # establish the range of x and y coordinates
    x_range = x_max - x_min
    y_range = y_max - y_min

    # in order to make sure the full eye is captured,
    # calculate the coordinates of a square that has a
    # 50% cushion added to the axis with a larger range and
    # then match the smaller range to the cushioned larger range
    if x_range > y_range:
        right = round(.5*x_range) + x_max
        left = x_min - round(.5*x_range)
        bottom = round((((right-left) - y_range))/2) + y_max
        top = y_min - round((((right-left) - y_range))/2)
    else:
        bottom = round(.5*y_range) + y_max
        top = y_min - round(.5*y_range)
        right = round((((bottom-top) - x_range))/2) + x_max
        left = x_min - round((((bottom-top) - x_range))/2)

    # crop the image according to the coordinates determined above
    cropped = frame[top:(bottom + 1), left:(right + 1)]

    # resize the image
    cropped = cv2.resize(cropped, (80, 80))
    image_for_prediction = cropped.reshape(-1, 80, 80, 3)

    return image_for_prediction

#TOKEN = '1953209547:AAGA_hx-6uCPlV1rQv4M9JdSYK3LORFdKRQ'
#bot = telegram.Bot(TOKEN)
# print(bot.get_me)


def webdetRec():
    TOKEN = '2111898018:AAH4VO7jvrz-aQxjeYSkM6z6NZcstPlE-1E'
    bot = telegram.Bot(TOKEN)
    account_sid = "AC68f7ede6200dc9fa01092066062b1cc8"
    auth_token  = "971defa7776a12d59a978fe242f6827f"
    client = Client(account_sid, auth_token)
    cap = cv2.VideoCapture(cv2.CAP_V4L2)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #subject = str("Driver Drowsiness")
    #msg = "Your Driver Was at Sleep Right Now"

    def sms():
        message = client.messages.create(
        to="+251934944167", 
        from_="+3197010253643",
        body="Your Driver was at drowsy! from you application")

    
    def send_email(subject, msg):
      server = smtplib.SMTP('smtp.gmail.com:587')
      server.ehlo()
      server.starttls()
      server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
      message = "\n\n subject: %s \n\n message:%s" % (subject, msg)
      server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)
      print("Success: Email Sent")
   

    # set a counter
    counter = 0
    # create a while loop that runs while webcam is in use
    while True:
        # capture frames being outputted by webcam
        ret, frame = cap.read()
        # use only every other frame to manage speed and memory usage
        frame_count = 0
        if frame_count == 0:
            frame_count += 1
            pass
        else:
            count = 0
            continue
        # function called on the frame
        image_for_prediction = eye_cropper(frame)
        try:
            image_for_prediction = image_for_prediction/255.0
        except:
            continue
        # get prediction from model
        prediction = eye_model.predict(image_for_prediction)
        # print(prediction)
        # Based on prediction, display either "Open Eyes" or "Closed Eyes"
        if (prediction[0][0] < 0.25) and (prediction[0][1] > 0.87):
            # print(prediction)
            counter = 0
            status = 'Normal'
            cv2.rectangle(frame, (round(w/2) - 110, 20),
                      (round(w/2) + 110, 80), (38, 38, 38), -1)
            cv2.putText(frame, status, (round(w/2)-80, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_4)
            x1, y1, w1, h1 = 0, 0, 175, 75
            # Draw black backgroun rectangle
            cv2.rectangle(frame, (x1, x1), (x1+w1-20, y1+h1-20), (0, 0, 0), -1)
            # Add text
            cv2.putText(frame, 'DDD', (x1 + int(w1/10), y1 +
                    int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            counter = counter + 1
            status = 'Closed'

            cv2.rectangle(frame, (round(w/2) - 110, 20),
                      (round(w/2) + 110, 80), (38, 38, 38), -1)

            cv2.putText(frame, status, (round(w/2)-104, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_4)
            x1, y1, w1, h1 = 0, 0, 175, 75
            # Draw black backgroun rectangle
            cv2.rectangle(frame, (x1, x1), (x1+w1-20, y1+h1-20), (0, 0, 0), -1)
            # Add text
            cv2.putText(frame, 'DDD', (x1 + int(w1/10), y1 +
                    int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # if the counter is greater than 3, play and show alert that user is asleep
            if counter > 5:
                

                # Draw black background rectangle
                cv2.rectangle(frame, (round(w/2) - 160, round(h) - 200),
                          (round(w/2) + 160, round(h) - 120), (0, 0, 255), -1)
                cv2.putText(frame, 'Wake up ', (round(w/2)-136, round(h) - 146),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_4)
                cv2.imshow('Drowsiness Detection', frame)
                k = cv2.waitKey(1)
                # Sound
                playsound('frist.wav ')
                
                #subject ="Driver Detection"
                #msg = "Your Driver was at Sleeping"
                #send_email(subject, msg)
                #sms()
                
                #tellegram
                #print(bot.get_me())
                #chat_id = bot.get_updates()[-1].message.chat_id
                #text = "Right Now the Driver was at sleep!Tell to him to take a break or stop driving"
                #bot.send_message(chat_id, text)

                counter = 1
                continue
        cv2.imshow('Drowsiness Detection', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def speaker_checker():
   mixer.init()
   alert=mixer.Sound('beep-07.wav')
   alert.play()
   time.sleep(0.3)
   alert.play()   
     
but1=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=web,text='Test Camera',font=('helvetica 15 bold'))
but1.place(x=5,y=104)

but2=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=speaker_checker,text='Check Speaker',font=('helvetica 15 bold'))
but2.place(x=5,y=176)

but4=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=webdetRec,text='Start the D3',font=('helvetica 15 bold'))
but4.place(x=5,y=250)

label_1 = Label(root, text="FullName",width=20,font=("bold", 10))
label_1.place(x=5,y=310)

entry_1 = Entry(root)
entry_1.place(x=240,y=310)

label_2 = Label(root, text="Email",width=20,font=("bold", 10))
label_2.place(x=5,y=340)

entry_2 = Entry(root)
entry_2.place(x=240,y=340)

label_3 = Label(root, text="Gender",width=20,font=("bold", 10))
label_3.place(x=5,y=370)

but5=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=exitt,font=('helvetica 15 bold'))
but5.place(x=210,y=478)


root.mainloop()






    








