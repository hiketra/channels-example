from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    first_child = models.ForeignKey('self', related_name='child_message', blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_message', blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


    def __unicode__(self):
        return ' [{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'id': self.message_id, 'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp, 'child': self.child_message, 'parent': self.parent_message}

