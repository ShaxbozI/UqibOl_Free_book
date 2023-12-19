import os
import shutil
import accounts.models
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from accounts.models import User, BookReview
from .models import (
    Author,
    AgeLimit, 
    Genres,
    SubGenres, 
    Language,
    Books,
    AudioFile,
    ReadFile,
    Links,
    )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birthdate', 'bio', 'picture' ]
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance



class AgeLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeLimit
        fields = '__all__'
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance



class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['id', 'genre', 'status']
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance



class SubGenresSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all(), required=True)
    class Meta:
        model = SubGenres
        fields = ['id', 'genre', 'sub_genres']
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance



class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance

     


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = BookReview
        fields = ['id', 'user', 'book', 'comment', 'stars_given']
        
    def validate(self, data):
        user = self.context['request'].user
        data['user'] = user
        return data
    
    def create(self, validated_data):
        book = validated_data['book'] 
        review = BookReview.objects.create(**validated_data)
        
        reviews = BookReview.objects.filter(book=book.id)
        if reviews:
            stars_sum = sum(review.stars_given for review in reviews) / len(reviews)
        else:
            stars_sum = 0
            
        book.stars_sum = stars_sum
        book.save()

        return review
        
    def update(self, instance, validated_data):
        for field in  self.Meta.fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
            
        return instance



class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'book', 'audio_file']

class ReadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadFile
        fields = ('id', 'book', 'read_file', )
    
class BooksSerializer(serializers.ModelSerializer):
    read_files = ReadFileSerializer(many=True, read_only=True)
    audio_files = AudioFileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['file', 'pdf', 'epub', 'doc', 'docx'])], allow_empty_file=False, use_url=False),
        write_only = True,
        required=False
    )
    uploaded_audios = serializers.ListField(
        child = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['audio', 'mp3', 'MP3'])], allow_empty_file=False, use_url=False),
        write_only = True,
        required=False
    )

    class Meta:
        model = Books
        fields = (
            'id', 
            'book_name', 
            'author', 
            'cost_status', 
            'genre', 
            'sub_genere', 
            'language', 
            'age_limit', 
            'info', 
            'year', 
            'publisher', 
            'is_audio', 
            'is_file',
            'stars_sum', 
            'read_count', 
            'cover_picture', 
            'read_files', 
            'uploaded_files', 
            'audio_files', 
            'uploaded_audios',
            )

    def validate(self, data):
        context = self.context
        is_create_action = context.get('request') and context['request'].method == 'POST'

        if is_create_action:
            author = data.get('author')
            uploaded_files = data.get('uploaded_files')
            uploaded_audios = data.get('uploaded_audios')

            if not author:
                raise serializers.ValidationError("Iltimos muallifni kiriting")
            
            if uploaded_files is None and uploaded_audios is None:
                raise serializers.ValidationError("Iltimos ushbu kitob uchun audio yoki file qo'shing")

        return data

    def create(self, validated_data):
        read_files_data = validated_data.pop('uploaded_files', [])
        audio_files_data = validated_data.pop('uploaded_audios', [])
        get_author = validated_data.get('author', None)
        book = Books.objects.create(**validated_data)

        for read_file in read_files_data:
            ReadFile.objects.create(book=book, read_file=read_file)

        for audio_file in audio_files_data:
            AudioFile.objects.create(book=book, audio_file=audio_file)
        
        if get_author:
            author = Author.objects.filter(id=get_author.id).first()
            author.book_count += 1
            author.save() 

        return book
    
    def update(self, instance, validated_data):
        # Avvalgi audio va filelarni o'chirib tashlash
        instance.read_files.all().delete()
        instance.audio_files.all().delete()
        
        fields = ('id', 'book_name', 'author', 'status', 'generes', 'sub_genere', 'age_limit', 'info', 'year', 'publisher', 'cover_picture', )
        for field in fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()

        read_files_data = validated_data.get('uploaded_files', [])
        audio_files_data = validated_data.get('uploaded_audios', [])

        if read_files_data:
            folder_path = f'media/book/{instance.set_name}/read_files'
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            for read_file in read_files_data:
                ReadFile.objects.create(book=instance, read_file=read_file)

        if audio_files_data:
            folder_path = f'media/book/{instance.set_name}/audio'
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
            for audio_file in audio_files_data:
                AudioFile.objects.create(book=instance, audio_file=audio_file)
            
        return instance
    
    
    
    


