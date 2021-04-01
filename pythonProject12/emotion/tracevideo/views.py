from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django import forms
from .models import Videos
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=250)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


def index(request):
    return render(request, 'tracevideo/index.html', {})
    # return JsonResponse([
    #     {
    #     'abc' : 'def',
    #     'ab': 'def',
    #     'ac': 'def',
    #     },
    #     {
    #         'abc': 'def',
    #         'ab': 'def',
    #         'ac': 'def',
    #     },
    #     {
    #         'abc': 'def',
    #         'ab': 'def',
    #         'ac': 'def',
    #     },
    #     {
    #         'abc': 'def',
    #         'ab': 'def',
    #         'ac': 'def',
    #     }
    # ], safe=False)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("abcd rupel")
            # handle_uploaded_file(request.FILES['file'])
            title = request.POST['title']
            video = request.FILES['file']
            content = Videos(title=title, video=video)
            content.save()
            return render(request, 'tracevideo/display.html', {
                'videos': Videos.objects.all()
            })
    else:
        form = UploadFileForm()
    return render(request, 'tracevideo/upload.html', {'form': form})


def display(request):
    # handle_uploaded_file()
    abc = Videos.objects.all()
    for a in abc:
        print(a.video.url + "rupel")
    return render(request, 'tracevideo/display.html', {
        'videos': Videos.objects.all()
    })

def play_xyz(request):

    video = Videos.objects.all()
    path = 'ImageBasic'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(classNames)

    #### FOR CAPTURING SCREEN RATHER THAN WEBCAM
    # def captureScreen(bbox=(300,300,690+300,530+300)):
    #     capScr = np.array(ImageGrab.grab(bbox))
    #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    #     return capScr

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture('http://127.0.0.1:8000/media/videos/xyz_FJb4XDi.mp4')
    while True:
        success, img = cap.read()
        print( f'sucess : {success}')
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name)

        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

    return HttpResponse("hello world")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        f.writelines(f'\n{name},{dtString}')