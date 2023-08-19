from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()


class Whiteboard(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "name"]),
        ]

class Drawing(models.Model):
    white_board = models.ForeignKey(Whiteboard, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=["white_board", "name"]),
        ]

class Action(models.Model):
    class ActionType(models.TextChoices):
        LINE = "line", _("line")
        SHAPE = "shape", _("shape")
        text = "text", _("text")
        
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    data = models.JSONField()
    index_number = models.PositiveIntegerField() # this for undo and redo action


    class Meta:
        indexes = [
            models.Index(fields=["drawing", "user"]),
        ]
