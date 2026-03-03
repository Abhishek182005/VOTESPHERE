from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    result_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='polls_created')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

    def winner(self):
        counts = {
            self.option_one: self.option_one_count,
            self.option_two: self.option_two_count,
            self.option_three: self.option_three_count,
        }
        return max(counts, key=counts.get)

    def percentage_one(self):
        t = self.total()
        return round((self.option_one_count / t) * 100, 1) if t else 0

    def percentage_two(self):
        t = self.total()
        return round((self.option_two_count / t) * 100, 1) if t else 0

    def percentage_three(self):
        t = self.total()
        return round((self.option_three_count / t) * 100, 1) if t else 0


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.CharField(max_length=20)  # 'option1', 'option2', 'option3'
    voted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll')  # one vote per user per poll

    def __str__(self):
        return f"{self.user.username} → {self.poll.question[:40]} [{self.choice}]"
