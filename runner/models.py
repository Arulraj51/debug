

from django.db import models

class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    buggy_code = models.TextField()
    expected_output = models.TextField()


    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class SolvedChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')