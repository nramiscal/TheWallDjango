from __future__ import unicode_literals
from django.db import models
from  django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
import bcrypt
import re
# re = regex

now = datetime.now()

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

class MessageManager(models.Manager):
    def msgValidator(self, message, id):
        errors = []

        if len(message) < 1:
            errors.append("Please input a message.")

        if len(errors) > 0:
            return (False, errors)
        else:
            message = Message.objects.create(message = message, author_id=id)
            return (True, message)


class CommentManager(models.Manager):
    def commentValidator(self, comment, author_id, message_id):
        errors = []

        if len(comment) < 1:
            errors.append("Please input a comment.")

        if len(errors) > 0:
            return (False, errors)
        else:
            comment = Comment.objects.create(comment = comment, author_id=author_id, message_id=message_id)
            return (True, comment)


class UserManager(models.Manager):
    def regValidator(self, form):
        errors = []

        if len(form['firstName']) < 3:
            errors.append("First name must be at least 3 characters.")
        elif not re.match('[A-Za-z]+', form['firstName']):
            errors.append("First name must only contain letters.")

        if len(form['lastName']) < 3:
            errors.append("Last name must be at least 3 characters.")
        elif not re.match('[A-Za-z]+', form['lastName']):
            errors.append("Last name must only contain letters.")

        if len(form['email']) < 1:
            errors.append("Email is required.")
        elif not ValidateEmail(form['email']):
            errors.append("Not a valid email.")
        elif User.objects.filter(email=form['email']):
            errors.append("Email address already in database.")

        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters.")

        if len(form['confirm_pw']) < 1:
            errors.append("Password confirmation is required.")
        if form['password'] != form['confirm_pw']:
            errors.append("Passwords do not match.")

        if len(errors) > 0:
            return (False, errors)
        else:
            pwhash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())

            user = User.objects.create(firstName = form['firstName'], lastName = form['lastName'], email = form['email'], password = pwhash)
            return (True, user)


    def loginValidator(self, form):
        errors = []
        email = form['email']
        password = form['password']

        if len(email) < 1:
            errors.append("Please input an email address.")
        elif not User.objects.filter(email=email):
            errors.append("This email is not registered in our database.")

        if len(password) < 1:
            errors.append("Please input a password.")

        if User.objects.filter(email=email):
            user = User.objects.get(email = email)
            if not bcrypt.hashpw(str(password), str(user.password)) == user.password:
                errors.append("Incorrect password: does not match password stored in database.")

        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.get(email = email)
            return (True, user)


class User(models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User {} {} {}>".format(self.firstName, self.lastName, self.email)

# User and Message have a one to many relationship
class Message(models.Model):
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name = "messages")
    objects = MessageManager()
    def __repr__(self):
        return "<Message {} {}>".format(self.message, self.author)


# Comment is the join table of User and Message
# User and Message have a many to many relationship
class Comment(models.Model):
    comment = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, related_name = "authors")
    message = models.ForeignKey(Message, related_name = "messages")
    objects = CommentManager()
    def __repr__(self):
        return "<Comment {} User_id = {} Message_id = {}>".format(self.comment, self.author_id, self.message_id)
