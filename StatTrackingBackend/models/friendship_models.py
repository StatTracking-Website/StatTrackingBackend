from datetime import datetime
from django.db import models
from multiselectfield import MultiSelectField

from StatTrackingBackend.models.user_models import User, ACCESS


class FriendshipManager(models.Manager):
    def befriend(self, user_from: User, user_to: User):

        if self.filter(user_from=user_from, user_to=user_to).exists():
            raise ValueError('Friendship already exists')

        self.create(user_from=user_from, user_to=user_to)
        self.create(user_from=user_to, user_to=user_from)

    def unfriend(self, user_from: User, user_to: User):
        self.filter(user_from=user_from, user_to=user_to).delete()
        self.filter(user_from=user_to, user_to=user_from).delete()

    def has_access(self, user_from: User, user_to: User, access: str):
        if user_from == user_to:
            return True
        if not access:
            return False
        if self.filter(user_from=user_from, user_to=user_to, access__contains=access).exists():
            return True
        return False


class Friendship(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_reversed')
    access = MultiSelectField(choices=ACCESS, max_length=256, blank=True)

    objects = FriendshipManager()

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f'{self.user_from} -> {self.user_to}'


class FriendshipRequestManager(models.Manager):
    def request_friendship(self, user_from: User, user_to: User, message: str):
        if user_from == user_to:
            raise ValueError('You cannot send a friendship request to yourself')
        if self.filter(user_from=user_from, user_to=user_to).exists():
            raise ValueError('Friendship request already exists')
        if Friendship.objects.filter(user_from=user_from, user_to=user_to).exists():
            raise ValueError('Friendship already exists')
        if self.filter(user_from=user_to, user_to=user_from).exists():
            self.accept_friendship(user_from=user_to, user_to=user_from)
            return
        self.create(user_from=user_from, user_to=user_to, message=message)

    def accept_friendship(self, user_from: User, user_to: User):
        friendship_request = self.filter(user_from=user_from, user_to=user_to)
        if not friendship_request.exists():
            raise ValueError('Friendship request does not exist')

        friendship_request.delete()
        Friendship.objects.befriend(user_from, user_to)

    def decline_friendship(self, user_from: User, user_to: User):
        friendship_request = self.filter(user_from=user_from, user_to=user_to)
        if not friendship_request.exists():
            raise ValueError('Friendship request does not exist')

        friendship_request.delete()


class FriendshipRequest(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    sent_on = models.DateTimeField(default=datetime.now(), blank=True)
    message = models.CharField(max_length=256, blank=True)

    objects = FriendshipRequestManager()

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f'{self.user_from} -> {self.user_to}'
