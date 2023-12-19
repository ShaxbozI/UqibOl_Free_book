import django.db.models
import os
import shutil
from django.urls import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from django.core.files.storage import default_storage
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from utility.custom_paginator import CustomPagination
from accounts.models import User, BookReview
from .serializers import (
    AuthorSerializer, 
    AgeLimitSerializer, 
    GenresSerializer,
    SubGenresSerializer, 
    LanguageSerializer,
    BookReviewSerializer,
    BooksSerializer,
    )

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




class AuthorCreateApiView(CreateAPIView):
    queryset = Author.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = AuthorSerializer 


class AuthorListApiView(ListAPIView):
    serializer_class = Author
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Author.objects.all()
    
    
class AuthorRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )
    
    
    

class AgeLimitCreateApiView(CreateAPIView):
    queryset = AgeLimit.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = AgeLimitSerializer
    
    
class AgeLimitListApiView(ListAPIView):
    serializer_class = AgeLimit
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return AgeLimit.objects.all()
    
    
class AgeLimitRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AgeLimit.objects.all()
    serializer_class = AgeLimitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )
    
    
    

class GenresCreateApiView(CreateAPIView):
    queryset = Genres.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = GenresSerializer
    
    
class GenresListApiView(ListAPIView):
    serializer_class = Genres
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Genres.objects.filter(status=True)
    
    
class GenresRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )
        
        
    
    
class SubGenresCreateApiView(CreateAPIView):
    queryset = SubGenres.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = SubGenresSerializer
    
    
class SubGenresListApiView(ListAPIView):
    serializer_class = SubGenres
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return SubGenres.objects.all()
    
    
class SubGenresRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubGenres.objects.all()
    serializer_class = SubGenresSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )
        
        
    
    
class LanguageCreateApiView(CreateAPIView):
    queryset = Language.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = LanguageSerializer
    
    
class LanguageListApiView(ListAPIView):
    serializer_class = Language
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Language.objects.all()
    
    
class LanguageRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )




class BookReviewApiView(CreateAPIView):
    queryset = BookReview.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = BookReviewSerializer
    
    
class BookReviewRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer  = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif muvofaqiyatli yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Muallif o'chirildi",
            }
        )
    
    
    
    

class BooksCreateApiView(CreateAPIView):
    queryset = Books.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = BooksSerializer
    
    
class BooksListApiView(ListAPIView):
    serializer_class = BooksSerializer
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Books.objects.all() 
    
    
class AudioBooksListApiView(ListAPIView):
    serializer_class = BooksSerializer
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Books.objects.filter(is_audio=True)
    
    
class ReadBooksListApiView(ListAPIView):
    serializer_class = BooksSerializer
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Books.objects.filter(is_file=True)
    
    
class KidsBooksListApiView(ListAPIView):
    serializer_class = BooksSerializer
    permission_classes = [AllowAny, ] 
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Books.objects.filter(age_limit__age_limit__lte = 14).order_by('read_count')
   
    
class BookRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def patch(self, request, *args, **kwargs):
        this_object = self.get_object()
        serializer = self.serializer_class(this_object, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Kitob yangilandi",
                'data': serializer.data
            }
        )
    
    def delete(self, request, *args, **kwargs):
        this_object = self.get_object()
        this_object.delete()
        return Response(
            {
                'success': True,
                'code': status.HTTP_200_OK,
                'message': "Kitob o'chirildi",
            }
        )


class AudioBookFilterApiView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = BooksSerializer
    pagination_class = CustomPagination

    def get(self, request, types, name):
        queryset = self.filter_books(types, name)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def filter_books(self, types, name):
        audio_books = Books.objects.filter(is_audio=True)
        if types == 'language':
            return audio_books.filter(language__language=name)
        
        if types == 'genre':
            return audio_books.filter(genre__genre=name)

        return audio_books
    

class ReadBookFilterApiView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = BooksSerializer
    pagination_class = CustomPagination

    def get(self, request, types, name):
        queryset = self.filter_books(types, name)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_books(self, types, name):
        read_books = Books.objects.filter(is_file=True)
        if types == 'language':
            return read_books.filter(language__language=name)
        
        if types == 'genre':
            return read_books.filter(genre__genre=name)

        return read_books
    
    
class KidsBookFilterApiView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = BooksSerializer
    pagination_class = CustomPagination

    def get(self, request, types, name):
        queryset = self.filter_books(types, name)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_books(self, types, name):
        kids_books = Books.objects.filter(age_limit__age_limit__lte = 14).order_by('read_count')
        if types == 'language':
            return kids_books.filter(language__language=name)
        
        if types == 'genre':
            return kids_books.filter(genre__genre=name)

        return kids_books
    
    
class BookFilterApiView(ListAPIView):
    queryset = Books.objects.all() 
    permission_classes = (AllowAny, )
    serializer_class = BooksSerializer
    pagination_class = CustomPagination

    def get(self, request, type):
        if type == 'all':
            books = Books.objects.all()
            readbooks = Books.objects.filter(is_file=True)
            audiobooks = Books.objects.filter(is_audio=True)
            read_alot = Books.objects.filter(is_file=True).order_by('read_count')
            listen_alot = Books.objects.filter(is_audio=True).order_by('read_count')
            child_books = Books.objects.filter(age_limit__age_limit__lte = 14).order_by('read_count')
            querysets = {
                'books': {'length': len(books), 'data': books},
                'readbooks': {'length': len(readbooks), 'data': readbooks},
                'audiobooks': {'length': len(audiobooks), 'data': audiobooks},
                'read_alot': {'length': len(read_alot), 'data': read_alot},
                'listen_alot': {'length': len(listen_alot), 'data': listen_alot},
                'child_books': {'length': len(child_books), 'data': child_books},
            }

            paginated_results = {}

            for key, queryset_data in querysets.items():
                serializer = self.serializer_class(queryset_data['data'], many=True)
                paginated_results[key] = {'length': queryset_data['length'], 'data': serializer.data}

            return Response(paginated_results, status=status.HTTP_200_OK)
        else:
            queryset = self.filter_books(type)
            if queryset:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.serializer_class(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response_data = {
                'info': "Iltimos mos filterlash parametrini kiriting",
                
                "Mos filterlar": {
                    'Barcha filterlar birga': reverse('book-filter', kwargs={'type': 'all'}),
                    
                    "Sahifalash imkoniyati mavjud": {
                        'Barcha kitoblar': reverse('book-filter', kwargs={'type': 'books'}),
                        "Faqat o'qish mumkin bo'lgan": reverse('book-filter', kwargs={'type': 'readbooks'}),
                        "Faqat tinglash mumkin bolgan": reverse('book-filter', kwargs={'type': 'audiobooks'}),
                        "Eng ko'p o'qilganlar": reverse('book-filter', kwargs={'type': 'read_alot'}),
                        "Eng ko'p eshitishlar": reverse('book-filter', kwargs={'type': 'listen_alot'}),
                        "Bolalar uchun": reverse('book-filter', kwargs={'type': 'child_books'}),
                    }
                }
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


    def filter_books(self, type):
        books = Books.objects.all()
        if type == 'readbooks':
            return books.filter(is_file=True)
        
        elif type == 'audiobooks':
            return books.filter(is_audio=True)
        
        elif type == 'read_alot':
            return books.filter(is_file=True).order_by('read_count')
        
        elif type == 'listen_alot':
            return books.filter(is_audio=True).order_by('read_count')
        
        elif type == 'child_books':
            return books.filter(age_limit__age_limit__lte = 14).order_by('read_count')
        
        elif type == 'books':
            return books
        
        else:
            return None




class AllCountsApiView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args):
        books = Books.objects.count()
        read_books = Books.objects.filter(is_file=True).count()
        audio_books = Books.objects.filter(is_audio=True).count()
        child_books = Books.objects.filter(age_limit__age_limit__lte = 14).order_by('read_count').count()
        authors = Author.objects.count()
        genres = Genres.objects.count()
        languages = Language.objects.count()
        audio_files = AudioFile.objects.count()
        read_file = ReadFile.objects.count()
        users = User.objects.count()
        reviews = BookReview.objects.count()
        
        response = {
            "Barcha kitoblar": books,
            "O'qish mumkin bo'lgan kitoblar": read_books,
            "Eshitish mumkin bo'lgan kitoblar": audio_books,
            "Bolalar uchun kitoblar": child_books,
            "Barcha Mualliflar": authors,
            "Barcha Janrlar": genres,
            "Barcha tillar": languages,
            "Barcha audio fayllar": audio_files,
            "Barcha o'qish mumkin bo'lgan fayllar": read_file,
            "Ro'yhatdan o'tgan Foydalanuvchilar": users,
            "Shu paytgacha yozilgan izohlar": reviews
        }
        return Response(response, status=status.HTTP_200_OK)
 


        
        
class ReadAndListenBookApiView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BooksSerializer
    
    def get(self, request, id):
        book = self.get_book(id)
        self.increment_read_count(request.user, book)

        reviews = BookReview.objects.filter(book=book.id)
        review_serializer = BookReviewSerializer(reviews, many=True)

        serializer = self.serializer_class(book)
        response_data = {
            'book_info': serializer.data,
            'reviews_count': len(reviews),
            'reviews': review_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

    def get_book(self, id):
        try:
            return Books.objects.get(id=id)
        except Books.DoesNotExist:
            raise Http404

    def increment_read_count(self, user, book):
        user_read_books = user.read_books.filter(id=book.id)
        if not user_read_books.exists():
            book.read_count += 1
            book.save()
            user.read_books.add(book)
        
        
        


class SearchBookApiView(ListAPIView):
    serializer_class = BooksSerializer
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        if search_query:
            search_book = Books.objects.filter(Q(book_name__icontains=search_query) | Q(author__first_name__icontains=search_query) | Q(author__last_name__icontains=search_query))
            if search_book:
                serializer = self.serializer_class(search_book, many=True)
                response = {
                    "search_query": search_query,
                    "count": len(serializer.data),
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
        
        response = {
            "search_query": search_query,
            "data": None
        }
        return Response(response, status=status.HTTP_200_OK)
