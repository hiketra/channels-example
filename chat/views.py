import random
import string
from django.db import transaction
from django.shortcuts import render, redirect
import haikunator
from .models import Room, Message

def about(request):
    return render(request, "chat/about.html")

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)

def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    threads = []

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    root_thread = Thread(True,
                         Message.objects.filter(parent__isnull=True),
                         None,
                         0)

    threads.append(root_thread)

    def createChildThreadsAndAppend(thread, tier):
        #takes in a thread and returns a list of thread objects of it's children
        childThreads = []
        parentMessages = thread.messages.filter(first_child__isnull = False)
        for message in parentMessages:
            threadMessages = room.messages.filter(parent = message.message_id).order_by('-timestamp')[:10]
            #unsure if this correct way of filtering
            parent_message = message.parent_message
            newThread = Thread(False, threadMessages, parent_message, tier)
            childThreads.append(newThread)
        return childThreads


    def childrenOfThreadList(threads, tier):
        #takes in a list of threads and returns a list of all their children
        childThreadLists = []
        for thread in threads:
            threadList = createChildThreadsAndAppend(thread, tier)
            childThreadLists.extend(threadList)

        return childThreadLists

    rootChildrenThreads = createChildThreadsAndAppend(root_thread, 1)
    secondTierChildrenThreads = childrenOfThreadList(rootChildrenThreads, 2)
    thirdTierChildrenThreads = childrenOfThreadList(secondTierChildrenThreads, 3)


    return render(request, "chat/room.html", {
        'room': room,
        'messages': threads
    })

class Thread(object):
    def __init__(self, is_root, messages, parent_message, children):
        self.is_root = is_root
        self.messages = messages
        self.parent_message = parent_message
        self.tier = 0 #thread-tree level
