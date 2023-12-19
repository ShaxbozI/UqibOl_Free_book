import os
import shutil
from typing import Any
import uuid
from django.db import models
from utility.utility import tr
from django.utils import timezone
from django.core.files.storage import default_storage


from django.core.validators import FileExtensionValidator



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    bio = models.TextField()
    picture = models.ImageField(upload_to=f'book/author', default='default_author_pic.png')
    book_count = models.PositiveIntegerField(default=0, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def author(self):
        return f"{self.first_name} {self.last_name}"

 
    
class Genres(models.Model):
    genre = models.CharField(max_length=20)
    # forum uchun ovoz yigish har haftada buning qiymati nolga tenglashtiriladi
    form_count = models.PositiveIntegerField(default=0, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.genre
    # Admin panelda chiquvchi nomi
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
    


class SubGenres(models.Model):
    genre = models.ForeignKey(Genres, models.CASCADE)
    sub_genres = models.CharField(max_length=20)
    # forum uchun ovoz yigish har haftada buning qiymati nolga tenglashtiriladi
    form_count = models.PositiveIntegerField(default=0, null=True)
    def __str__(self):
        return self.sub_genres
    # Admin panelda chiquvchi nomi
    class Meta:
        verbose_name = "SubGenre"
        verbose_name_plural = "SubGenres"


    
class Language(models.Model):
    language = models.CharField(max_length=30)
    def __str__(self):
        return self.language



class AgeLimit(models.Model):
    age_limit = models.IntegerField()
    def __int__(self):
        return self.age_limit
    def __str__(self):
        return str(self.age_limit)



class SetNameId(models.Model):
    set_id = models.UUIDField()
    def save(self, *args, **kwargs):
        if not self.set_id:
            self.set_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.set_id)



class Books(models.Model):
    class Status(models.TextChoices):
        Payment = 'P', 'Payment'
        Free = 'F', 'Free'
        
    def file_upload_to(instance, filename, path):
        extension = filename.split('.')[-1]
        new_filename = f'{instance.set_name}.{extension}'
        return f'book/{instance.set_name}/{path}/{new_filename}'
    
    def audio_file_upload_to(instance, filename):
        return instance.file_upload_to(filename, 'audio')
    
    def read_file_upload_to(instance, filename):
        return instance.file_upload_to(filename, 'read_file')
    
    def cover_picture_upload_to(instance, filename):
        return instance.file_upload_to(filename, 'photo')
    
    book_name = models.CharField(max_length=300)
    set_name = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    info = models.TextField()
    
    audio_file = models.FileField(upload_to=audio_file_upload_to, null=True, blank=True, default='')
    read_file = models.FileField(upload_to=read_file_upload_to, null=True, blank=True, default='')
    
    cost_status = models.CharField(max_length=1, choices=Status.choices, default=Status.Free)
    language = models.ForeignKey(Language, models.CASCADE)
    genre = models.ForeignKey(Genres, models.CASCADE)
    sub_genere = models.ForeignKey(SubGenres, models.CASCADE)
    age_limit = models.ForeignKey(AgeLimit, on_delete=models.SET_DEFAULT, default=1)
    
    year = models.IntegerField()
    publisher = models.CharField(max_length=200)
    cover_picture = models.ImageField(upload_to=cover_picture_upload_to, default='default_book_pic.png')
    
    # auto fieldlar
    read_count = models.IntegerField(default=0)
    # forum uchun ovoz yigish har haftada buning qiymati nolga tenglashtiriladi
    form_count = models.PositiveIntegerField(default=0, null=True)
    stars_sum = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    is_audio = models.BooleanField(default=False)
    is_file = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if Books.objects.filter(pk=self.pk).exists():
            # Eski rasmini olish
            previous_instance = Books.objects.get(pk=self.pk)
            if previous_instance.photo:
                previous_path = previous_instance.photo.path
                # Obyektning eski rasimini o'chiramiz.
                default_storage.delete(previous_path)
        
        else:
            tr_id = SetNameId.objects.last().id if SetNameId.objects.last() else 0
            self.set_name = f'user_{tr_id:09d}'
            SetNameId.objects.create()
            
        # o'zgarishlar va yangi rasmni avtomatik xos nom bilan saqlanadi
        super(Books, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        folder_path = f'media/book/{self.set_name}'
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        
        super().delete(*args, **kwargs)
            
    # Admin panelda chiquvchi nomi
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        return self.book_name
    
    


class AudioFile(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='audio_files')
    
    def book_set_name(instance, filename): 
        get_book = Books.objects.get(id=instance.book.id)
        return f'book/{get_book.set_name}/audio/{filename}'
    
    audio_file = models.FileField(
        upload_to=book_set_name,
        validators=[FileExtensionValidator(allowed_extensions=['audio', 'mp3', 'MP3'])],
        )
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if self.book and not self.book.is_audio:
            self.book.is_audio = True
            self.book.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        folder_path = f'media/book/{self.set_name}/audio'
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        
        super().delete(*args, **kwargs)
        
    
    

class ReadFile(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='read_files')
    
    def book_set_name(instance, filename): 
        get_book = Books.objects.get(id=instance.book.id)
        return f'book/{get_book.set_name}/read_files/{filename}'
    
    read_file = models.FileField(
        upload_to=book_set_name,
        validators=[FileExtensionValidator(allowed_extensions=['file', 'pdf', 'epub', 'doc', 'docx'])],
        )
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if self.book and not self.book.is_file:
            self.book.is_file = True
            self.book.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        folder_path = f'media/book/{self.set_name}/read_files'
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        
        super().delete(*args, **kwargs)
            
    
    



class Links(models.Model):
    class TypeLink(models.TextChoices):
        Buy = 'B', 'Buy'
        Read = 'R', 'Read'
        Listen = 'L', 'Listen'
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    type_link = models.CharField(max_length=1, choices=TypeLink.choices)
    link_name = models.CharField(max_length=300)
    link = models.URLField()
    def __str__(self):
        return f'{self.book.set_name} || link-name:: ({self.link_name})'
    
    # Admin panelda chiquvchi nomi
    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    

