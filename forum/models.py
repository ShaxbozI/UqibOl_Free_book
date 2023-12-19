from django.db import models
from books.models import Books
from accounts.models import User
from django.utils import timezone




# Haftaning shanba kunlari avtomatik bir yangi forum ochiladi va bu shu kuning o'zida yopiladi
class Forum(models.Model):
    book = models.ForeignKey(Books, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def book_set_name(self):
        get_book = Books.objects.filter(id = self.book.id)
        return get_book.set_name
    
    
    
# Forumda yoyiladigan izoh va fikrlar uchun.
class ForumReview(models.Model):
    forum = models.ForeignKey(Forum, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    reiew = models.TextField()