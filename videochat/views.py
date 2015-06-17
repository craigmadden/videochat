from django.shortcuts import render, render_to_response, redirect
from .models import Chat, Contact
from .forms import UserForm, ChatForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
import uuid

# Create your views here.
def home(request):
    context = RequestContext(request)
    contacts = Contact.objects.all()
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        chat_form = ChatForm(data=request.POST)
        #import pdb; pdb.set_trace()
        #if chat_form.is_valid():
        # Build the Chat object with a uuid
        chat_uuid = uuid.uuid4()
        chat = Chat(chatname=chat_uuid)
        chat.save()

        # If user is logged in, check if a contact id was passed
        # Redirect to the chat passing the uuid
        return redirect('chat',chat_uuid)
    # Not a HTTP POST, so we render our form using the ModelForm.
    # These forms will be blank, ready for user input.
    else:
        chat_form = ChatForm()

	#return render(request, 'videochat/home.html',{'chat_form':chat_form,'contacts':contacts})
    return render_to_response('videochat/home.html', {'contacts':contacts}, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
            'videochat/register.html',
            {'user_form': user_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your WebRTC account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied. <a href='login'>Please try again</a>")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('videochat/login.html', {}, context)


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

def chat(request,uuid):
    context = RequestContext(request)
    # Query the database and retrieve the chat details for uuid
    chatter = Chat.objects.all().get(chatname=uuid)
    # Do webrtc magic here ????
    return render_to_response('videochat/chat.html',{'chatter':chatter},context)