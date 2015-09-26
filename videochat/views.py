from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from .models import Chat, Contact
from .forms import UserForm, ChatForm, EditContactForm, AddContactForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
import uuid
import random

# Create your views here.
def home(request):
    context = RequestContext(request)
    user = request.user
    contacts = Contact.objects.filter(user_id=user.id)
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        chat_form = ChatForm(data=request.POST)
        #import pdb; pdb.set_trace()
        # Build the Chat object with a uuid
        chatid = request.POST['chatname']
        contact = False
        if chatid:
            return redirect('chat',chatid)
        elif contact:
            pass
        else:
            #chat_uuid = uuid.uuid4()
            unique_chat_id = True
            chat_uuid = random.randrange(30000,60000)
            # Check if this chat id has already been used
            while unique_chat_id:
                if Chat.objects.all().filter(chatname=chat_uuid):
                    chat_uuid = random.randrange(30000,60000)
                else:
                    chat = Chat(chatname=chat_uuid)
                    chat.save()
                    unique_chat_id = False
            

            # If user is logged in, check if a contact id was passed
            # Redirect to the chat passing the uuid
            return redirect('chat',chat_uuid)

    # Not a HTTP POST, so we render our form using the ModelForm.
    # These forms will be blank, ready for user input.
    else:
        chat_form = ChatForm()

	#return render(request, 'videochat/home.html',{'chat_form':chat_form,'contacts':contacts})
    return render_to_response('videochat/home.html', {'contacts':contacts}, context)

def user_profile(request):
    context = RequestContext(request)
    user = request.user
    contacts = Contact.objects.filter(user_id=user.id)

    if request.method == 'POST':
        contact_element = request.POST['contact-email'].partition(':')
        contact_email = contact_element[2].lstrip()
        return redirect('edit_contact',contact_email)
    else:
        return render_to_response('videochat/profile.html', {'contacts':contacts}, context)

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
    user = request.user
    contacts = Contact.objects.filter(user_id=user.id)
    # Query the database and retrieve the chat details for uuid
    chatter = Chat.objects.all().get(chatname=uuid)
    # If chat status is waiting, call the chat_join.html template
    if chatter.chat_status == "Waiting":
        return render_to_response('videochat/chat_join.html',{'chatter':chatter},context)
    elif chatter.chat_status == "Initialize":
        # If chat status is initializing, call the chat_init.html template
        return render_to_response('videochat/chat_init.html',{'chatter':chatter,'contacts':contacts},context)
    
def update_status(request):
    # Update status of specified Chat
    uuid = request.POST['uuid']
    status = request.POST['status']
    chat = Chat.objects.all().get(chatname=uuid)
    chat.chat_status=status
    chat.save()
    return HttpResponse("Status set to: " + status)

def edit_contact(request,contact_email):
    context = RequestContext(request)
    contact = Contact.objects.all().get(email=contact_email)
    
    if request.method == 'POST':
        if 'save-edit' in request.POST:
            post = get_object_or_404(Contact, pk=contact.id)
            # Get values of form and update database
            form = EditContactForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                
        elif 'delete-contact' in request.POST:
            post = get_object_or_404(Contact, pk=contact.id).delete()

        return redirect('/profile')
    else:
        edit_contact_form = EditContactForm(instance=Contact.objects.all().get(email=contact_email))
        if contact:
            return render(request, 'videochat/edit_contact.html', locals())
        else:
            return HttpResponseRedirect('/')

def add_contact(request):
    context = RequestContext(request)
    if request.method == 'POST':
        # Save contents of form

        contact_form = AddContactForm(data=request.POST)

        # If the two forms are valid...
        if contact_form.is_valid():
            # Save the user's form data to the database.
            contact = contact_form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('/profile')
    else:
        # Present New Contact form
        add_contact_form = AddContactForm()

    # Render the template depending on the context.
    return render_to_response(
            'videochat/contact.html',
            {'add_contact_form': add_contact_form},
            context)

def end_chat(uuid):
    # Update chat_status to Terminated
    chat = Chat.objects.all().get(chatname=uuid)
    chat.chat_status="Terminated"
    chat.save()
    return redirect('/')