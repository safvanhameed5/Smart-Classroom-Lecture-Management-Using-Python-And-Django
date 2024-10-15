from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.contrib import messages

from .models import *


def login(request):
    return render(request, 'login.html')


def detector():
    import cv2
    import numpy as np

    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("trainingData.yml")
    id = 0
    val=0
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 1
    fontcolor = (255, 255, 255)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])

            if (id > 0):
                val=id
                break
            else:
                val=0
            cv2.putText(img, str(id), (x, y + h), font, fontscale, fontcolor)
        cv2.imshow('Face', img)
        if (cv2.waitKey(1) == ord('q') or id > 0):
            break

    cam.release()
    cv2.destroyAllWindows()
    return(val)


def logindb(request):
    id = detector()
    print(id)

    us_reg = UserReg.objects.filter(id=id)
    if us_reg.count() > 0:
        for ur in us_reg:
            request.session['uid'] = ur.id
            request.session['email'] = ur.Email

        return redirect('/App/home/')
    elif id==0:
        messages.error(request, 'Username or password not mach')
        return HttpResponseRedirect(reverse('Login'))
    # uname = request.POST['username']
    # psw = request.POST['password']
    # us_reg = UserReg.objects.filter(Username=uname, Password=psw)
    # if us_reg.count() > 0:
    #     for ur in us_reg:
    #         request.session['uid'] = ur.Details_id
    #         request.session['email'] = ur.Username
    #
    #     return redirect('/home/')
    # messages.error(request, 'Username or password not mach')
    # return HttpResponseRedirect(reverse('Login'))
    # pass


def register(request):
    return render(request, 'register.html')
    pass


def datacreator(uid):
    import cv2
    import numpy as np

    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    id = uid
    sampleNum = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1
            cv2.imwrite("D:/MyClassroom/Classroom/myclassroomapp/dataSet/User." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow('Face', img)
        cv2.waitKey(1)
        if (sampleNum > 20):
            break

    cv2.destroyAllWindows()
    cam.release()
    return(1)


def createtrainer():
    import os
    import cv2
    import numpy as np
    from PIL import Image

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'D:/MyClassroom/Classroom/myclassroomapp/dataSet'

    def getImageWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            """print ID"""
            IDs.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImageWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save("trainingData.yml")
    cv2.destroyAllWindows()


def registerdb(request):
    name = request.POST['name']
    phone = request.POST['phone']
    username = request.POST['username']
    password = request.POST['password']
    usr = UserReg(Name=name, Phone=phone,
                      Email=username,Password=password)
    usr.save()
    last_usr = UserReg.objects.latest('id').id
    data=datacreator(last_usr)
    createtrainer()
    return HttpResponseRedirect(reverse('Login'))


def home(request):
    data =modulereg.objects.filter(Userid=request.session['uid']).values()
    context = {
        'data':data
    }
    return render(request, 'medicadd.html',context)


def moduledb(request):
    module = request.POST['module']
    title = request.POST['title']
    data = modulereg(Userid=get_object_or_404(UserReg,pk=request.session['uid']), Module_number=module, Module_title=title)
    data.save()
    return HttpResponseRedirect(reverse('user_home'))


def viewnotes(request,id):
    request.session['mid'] = id
    data = notereg.objects.filter(moduleid=id).values()
    context = {
        'data': data
    }
    print(context)
    return render(request, 'notes.html', context)


def notesdb(request):
    title = request.POST['title']
    file = request.FILES['file']
    data = notereg(Userid=get_object_or_404(UserReg, pk=request.session['uid']),moduleid=get_object_or_404(modulereg, pk=request.session['mid']),
                     Note_title=title,notefile=file)
    data.save()
    return redirect('/App/notes/'+request.session['mid'])


def logout(request):
    try:
        del request.session['uid']
        del request.session['email']
    except KeyError:
        pass
    return redirect('/App/')


def downloadfile(request,path):
    return None