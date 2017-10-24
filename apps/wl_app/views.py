from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from models import User, UserManager, Message, Comment, MessageManager, CommentManager
from datetime import datetime
# from time import localtime, strftime, gmtime
import bcrypt


def index(request):
    # User.objects.all().delete()
    # Message.objects.all().delete()
    # Comment.objects.all().delete()
    return render(request, 'wl_app/index.html')


def register(request):
    val = User.objects.regValidator(request.POST)

    if val[0]:
        request.session['name'] = val[1].firstName
        request.session['id'] = val[1].id
        messages.add_message(request, messages.SUCCESS, "User successfully registered.")
        messages.add_message(request, messages.SUCCESS, "Please log in.")
        return redirect('/')
    else:
        for error in val[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')


def login(request):
    val = User.objects.loginValidator(request.POST)

    if val[0]:
        request.session['id'] = val[1].id
        request.session['name'] = val[1].firstName
        return redirect('/wall')
    else:
        for error in val[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

def wall(request):
    posts = Message.objects.order_by("-created_at")
    comments = Comment.objects.all()
    # now = strftime("%a, %d %b %Y %H:%M", gmtime())
    return render(request, 'wl_app/wall.html', {"posts": posts, "comments": comments})

def createMessage(request):
    val = Message.objects.msgValidator(request.POST['message'], request.session['id'])

    if val[0]:
        return redirect('/wall')
    else:
        for error in val[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/wall')

def createComment(request):
    val = Comment.objects.commentValidator(request.POST['comment'], request.session['id'], request.POST['message_id'])

    if val[0]:
        return redirect('/wall')
    else:
        for error in val[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/wall')


def logout(request):
    request.session.clear()
    return redirect('/')


def deleteMessage(request, message_id):

    # timeCreated = Message.objects.get(id=message_id).created_at
    # now = timezone.now()
    # diff = now - timeCreated

    Message.objects.get(id = message_id).delete()
    return redirect('/wall')
