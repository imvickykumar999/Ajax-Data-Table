from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])

    def __str__(self):
        return self.question_text

class Solution(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    def __str__(self):
        return f"Options for: {self.question.question_text}"
