from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    text = models.TextField(blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = ('Message')
        verbose_name_plural = ('Messages')

    def __str__(self):
        return self.text

    # def get_absolute_url(self):
    #     return reverse('add_message', args=[str(TodoList.pk)])


class TodoList(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(Category, default='general', on_delete=models.PROTECT)
    user = models.CharField(max_length=50)
    message = models.ManyToManyField(Message, blank=True)

    class Meta:
        ordering = ['due_date']

    def get_absolute_url(self):
        return reverse('todo-detail', args=[str(self.id)])

    def __str__(self):
        return self.title
