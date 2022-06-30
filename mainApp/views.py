from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
import smtplib
from email.message import EmailMessage
import random
from django.contrib.auth import authenticate, login, logout
from .models import otp, HomeworkUploads, Preferences, Notifications, Quotes, Question, Note
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from slugify import slugify
import requests
from django.views.decorators.csrf import csrf_exempt



def index(request):
    if request.method == 'POST':
        print(User.objects.filter(username='2213yash', password='yashverma'))
        name = request.POST['username']
        passuser = request.POST['pass']
        print(passuser)
        loginuser = authenticate(request, username=name, password=passuser)
        print(loginuser)
        if loginuser is not None:
            login(request, loginuser)
            return redirect('/home')
        else:
            return HttpResponse('incorrect')
    user = request.user
    if user.is_authenticated:
        return redirect('/home')
    return render(request, 'login.html')


def sendMail(email, name):
    EMAIL_ADDRESS = '2213yash@gmail.com'
    EMAIL_PASSWORD = 'vlsgiqvysdtxasnk'
    verifyotp = random.randrange(10000, 99999)
    saveotp = otp(email = email, otp = verifyotp)
    saveotp.save()
    msg = EmailMessage()
    msg['Subject'] = f'{verifyotp}'
    msg['From'] = "Chakwal 12A<2213yash@gmail.com>"
    msg['To'] = email
    msg.set_content(f'''
    <!DOCTYPE html>
    <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
        </head>
        <body>
            <div class="container" style="padding: 20px;">
           <div class="otp" style="text-align: center;">
            <h2 style="color: crimson; font-family: 'poppins', sans-serif;">{verifyotp}</h2>
        </div>
        <div class="para" style="text-align: left;">
            <p style="font-family: 'poppins', sans-serif; font-size: 20px; color: rgb(41, 39, 40);">Hello {name}, Thanks for registering with Chakwal 12A. Your One Time Password for login is {otp}. After Verify Kindly Login With Your Credentials. This OTP is valid for 24 hrs.</p>
            <p>- Chakwal 12A Team</p>
        </div>
    </div>
        </body>
    </html>
    ''', subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print('mail sent')


def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST["email"]
        password = request.POST['password']
        password2 = request.POST['confpassword']

        if password == password2:
            checkuser = User.objects.filter(username = username).first()
            if checkuser is None:
                checkemail = User.objects.filter(email = email).first()
                if checkemail is None:
                    if len(password) < 8:

                        doc = {
                            'message' : 'passwords must consist of least 8 charaters.'
                        }
                        return render(request, 'signup.html', doc)
                    else:
                        try:
                            saveuser = User.objects.create_user(username = username, email = email)
                            saveuser.set_password(password)
                            saveuser.first_name = first_name
                            saveuser.last_name = last_name
                            saveuser.is_active = False
                            saveuser.save()
                            sendMail(email = email, name = first_name)
                            redirectuser = redirect('/verify')
                            redirectuser.set_cookie('email', email)
                            redirectuser.set_cookie('username', username)
                            redirectuser.set_cookie('password', password)
                            return redirectuser
                        except Exception as e:
                            doc = {
                                'message' : 'Something went wrong. Please try again later...'
                            }
                            return render(request, 'signup.html', doc)
                else:
                    doc = {
                        'message' : "Email Already in Use."
                    }
                    return render(request, 'signup.html', doc)
            else:
                doc = {
                    "message" : "User already exists. Please choose another username"
                }
                return render(request, 'signup.html', doc)
        else:
            doc = {
                    "message" : "Your passwors don't match. Try again..."
                }
            return render(request, 'signup.html', doc)
    return render(request, 'signup.html')


def home(request):
    user = request.user
    if user.is_authenticated:
        doc = {
            'user' : user.first_name
        }
        return render(request, 'home.html', doc)
    return redirect('/')

def verify(request):
    getemail = request.COOKIES['email']
    if getemail is None:
        return redirect('/')
    else:
        if request.method == 'POST':
            user = request.user
            getotp = request.POST.get('otp')
            verifyotp = otp.objects.filter(otp=getotp, email = getemail).first()
            if verifyotp == None:
                return HttpResponse('incorrect')
            else:
                verifyotp.delete()
                redirectuseragain = redirect('/home')
                username = request.COOKIES['username']
                getusername = User.objects.get(username = username)
                getusername.is_active = True
                getusername.save()
                return redirect('/')
        email = request.COOKIES['email']
        doc= {
            'email' : email
        }
        return render(request, 'otp.html', doc)

def logoutUser(request):
    logout(request)
    return redirect('/')

def Homework(request):
    user = request.user
    if user.is_authenticated:
        homeworks = HomeworkUploads.objects.all().order_by('-date')
        doc = {
            'homework' : homeworks,
            'user' : user
        }
    return render(request, 'homework.html', doc)

def UploadHomework(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':

            title = request.POST.get('title')
            subject = request.POST.get('subject')
            files = request.FILES['file']
            desc = request.POST.get('desc')
            slug = slugify(title)
            if files.content_type == "application/pdf":
                uploadfile = HomeworkUploads(title = title, user = user, files = files, subject = subject, slug= slug, desc=desc)
                uploadfile.save()
                messages.success(request, 'Homework Uploaded Successfully !!!')
                return redirect('/homework')
            else:
                messages.error(request, 'Only PDF files are accepted...')
                return redirect('/homework/upload')
        return render(request, 'uploadHomework.html')
    else:
        return redirect('/')
    return redirect('/')

def DowloadHomework(request):
    user = request.user
    if user.is_authenticated:
        homeworks = HomeworkUploads.objects.all()
        doc = {
            'homework' : homeworks
        }
        return render(request, 'Downloadhomework.html', doc)
    return redirect('/')


def postLikes(request):
    user = request.user
    post = request.POST.get('homework')
    lol = HomeworkUploads.objects.get(title = post)
    if user.is_authenticated:
        #  get the post parameters
        user = request.user
        Preference = request.POST.get('preference')
        finduser = Preferences.objects.filter(user = user, post = lol).first()
        if finduser:
            userprefrence = finduser.preference
            if userprefrence == 1:
                finduser.preference = 0
                finduser.save()
                lol.likes = lol.likes - 1
                lol.save()
            elif userprefrence == 0:
                finduser.preference = 1
                finduser.save()
                lol.likes = lol.likes + 1
                lol.save()
            return redirect(f'/homework')
        else:
            savelike = Preferences(user = user, post = lol, preference = Preference)
            savelike.save()
            lol.likes = lol.likes + 1
            lol.save()
            return redirect(f'/homework')
    messages.warning(request, 'Please Signup For Like And More Features !')
    return redirect(f'/{lol.slug}')

def Chat(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'chat.html', {
            'user' : user
        })
    return redirect('/')

def Notification(request):
    user = request.user
    if user.is_authenticated:
        allnoto = Notifications.objects.all().order_by('-date')
        doc = {
            'noti' : allnoto
        }
        return render(request, 'notifications.html', doc)
    return redirect('/')

def Motivations(request):
    user = request.user
    if user.is_authenticated:
        motis = Quotes.objects.all()
        count = Quotes.objects.count()
        random_object = Quotes.objects.all()[random.randint(0, count - 1)]
        print(random_object)
        doc = {
            'motivation' : random_object
        }
        return render(request, 'motivation.html', doc)
    return redirect('/')

def profile(request):
    user = request.user
    if user.is_authenticated:
        users = user
        doc = {
            'user' : users
        }
        return render(request, 'profile.html')
    return redirect('/')

def changeProfile(request):
    if request.method == 'POST':
        print('ok')
        fname = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        try:
            finduser = User.objects.get(username = request.user)
            finduser.first_name = fname
            finduser.last_name = last_name
            finduser.save()
            messages.success(request, 'Details changed successfully !')
            return redirect('/profile')
        except Exception as e:
            messages.error(request, 'Internal server error... please try again later')
            return redirect('/profile')
    return redirect('/')

@csrf_exempt

def fetchLikes(request):
    if request.method == 'POST':
        users= request.POST.get('user')
        post = request.POST.get('post')
        convertpost = list(post.split(","))
        finduser = User.objects.filter(username = users).first()
        convertpost.pop()
        likeCount = []
        for i in convertpost:
            try:
                isUserLiked = Preferences.objects.get(post = i, user=finduser).preference
                likeCount.append(isUserLiked)

            except Preferences.DoesNotExist as e:
                isUserLiked = 0
                likeCount.append(isUserLiked)
        print(likeCount)
        return JsonResponse({'likesValues' : likeCount})
    return JsonResponse({'message' : 'invalid request'})


def questions(request):
    user = request.user
    if user.is_authenticated:
        question = Question.objects.all().order_by('-date')
        doc = {
            'ques' : question
        }
        return render(request, 'questions.html', doc)
    return redirect('/')

def sendReport(email, name, post):
    EMAIL_ADDRESS = '2213yash@gmail.com'
    EMAIL_PASSWORD = 'vlsgiqvysdtxasnk'
    msg = EmailMessage()
    msg['Subject'] = f'Report Successfull'
    msg['From'] = "Chakwal 12A<2213yash@gmail.com>"
    msg['To'] = email
    msg.set_content(f'''
    <!DOCTYPE html>
    <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
        </head>
        <body>
           <div class="container" style="padding: 20PX;text-align: left;">
               <p style="font-size: 15px; font-family: 'poppins', sans-serif; color: rgb(67, 67, 190);">hello {name}, we are glad to recieve your report. we are trying to find out the problem in {post} as soon as possible. Once the problem is found, it will be solved.</p>
               <p>- Chakwal 12A Team</p>
           </div>
        </body>
    </html>
    ''', subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print('mail sent')

def report(request):
    if request.method == 'POST':
        post = request.POST.get('post')
        email = request.user.email
        name = request.user.first_name
        sendReport(email, name, post)
        messages.success(request, 'Reported Successfully')
        return redirect('/homework')
    return redirect('/')

def notes(request):
    user = request.user
    if user.is_authenticated:
        notes = Note.objects.all().order_by('-date')
        doc = {
            'notes' : notes
        }
        return render(request, 'notes.html', doc)
    return redirect('/')