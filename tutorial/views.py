# import time
from datetime import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datetime_safe import time

from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_my_events
from tutorial.outlookservice import get_my_contacts
from tutorial.outlookservice import get_my_messages
from tutorial.outlookservice import get_me
def home(request):
  return HttpResponse("Welcome to the tutorial.")

# def home(request):
#   sign_in_url = '#'
#   context = { 'signin_url': sign_in_url }
#   return render(request, 'tutorial/home.html', context)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url

# Create your views here.

def home(request):
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = { 'signin_url': sign_in_url }
  return render(request, 'tutorial/home.html', context)

# def gettoken(request):
#   return HttpResponse('gettoken view')

# def gettoken(request):
#   auth_code = request.GET['code']
#   return HttpResponse('Authorization code: {0}'.format(auth_code))
#
# # Add import statement to include new function
from tutorial.outlookservice import get_me

# def gettoken(request):
#   auth_code = request.GET['code']
#   redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
#   token = get_token_from_code(auth_code, redirect_uri)
#   access_token = token['access_token']
#   user = get_me(access_token)
#
#   # Save the token in the session
#   request.session['access_token'] = access_token
#   return HttpResponse('User: {0}, Access token: {1}'.format(user['displayName'], access_token))

# Add import statement to include new function
from tutorial.outlookservice import get_me

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  return HttpResponseRedirect(reverse('tutorial:mail'))
  # return HttpResponse('User: {0}, Access token: {1}'.format(user['displayName'], access_token))

# def gettoken(request):
#   auth_code = request.GET['code']
#   redirect_uri = request.build_absolute_uri(reverse('tutorial:gettoken'))
#   token = get_token_from_code(auth_code, redirect_uri)
#   access_token = token['access_token']
#   user = get_me(access_token)
#   refresh_token = token['refresh_token']
#   expires_in = token['expires_in']
#
#   # expires_in is in seconds
#   # Get current timestamp (seconds since Unix Epoch) and
#   # add expires_in to get expiration time
#   # Subtract 5 minutes to allow for clock differences
#   expiration = int(time.time()) + expires_in - 300
#
#   # Save the token in the session
#   request.session['access_token'] = access_token
#   request.session['refresh_token'] = refresh_token
#   request.session['token_expires'] = expiration
#   return HttpResponseRedirect(reverse('tutorial:mail'))

# def mail(request):
#   access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
#   # If there is no token in the session, redirect to home
#   if not access_token:
#     return HttpResponseRedirect(reverse('tutorial:home'))
#   else:
#     return HttpResponse('Access token found in session: {0}'.format(access_token))

# def mail(request):
#   access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
#   # If there is no token in the session, redirect to home
#   if not access_token:
#     return HttpResponseRedirect(reverse('tutorial:home'))
#   else:
#     messages = get_my_messages(access_token)
#     return HttpResponse('Messages: {0}'.format(messages))
def mail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    messages = get_my_messages(access_token)
    context = { 'messages': messages['value'] }
    return render(request, 'tutorial/mail.html', context)

def events(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    events = get_my_events(access_token)
    context = { 'events': events['value'] }
    return render(request, 'tutorial/events.html', context)

def contacts(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('tutorial:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('tutorial:home'))
  else:
    contacts = get_my_contacts(access_token)
    context = { 'contacts': contacts['value'] }
    return render(request, 'tutorial/contacts.html', context)