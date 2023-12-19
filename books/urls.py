from bookinfo.views import InfoPageView
from .views import *
from django.urls import path

urlpatterns = [
    path('add/author/', AuthorCreateApiView.as_view(), name='add_author'),
    path('add/agelimit/', AgeLimitCreateApiView.as_view(), name='add_agelimit'),
    path('add/genre/', GenresCreateApiView.as_view(), name='add_genre'),
    path('add/language/', LanguageCreateApiView.as_view(), name='add_language'),
    path('add/subgenre/', SubGenresCreateApiView.as_view(), name='add_subgenre'),
    path('add/book', BooksCreateApiView.as_view(), name='add_book'),
    path('add/review/', BookReviewApiView.as_view(), name='add_review'),
    
    path('edit/author/<int:pk>/', AuthorRetriveUpdateDestroyView.as_view(), name='edit_author'),
    path('edit/agelimit/<int:pk>/', AgeLimitRetriveUpdateDestroyView.as_view(), name='edit_agelimit'),
    path('edit/genre/<int:pk>/', GenresRetriveUpdateDestroyView.as_view(), name='edit_genre'),
    path('edit/language/<int:pk>/', LanguageRetriveUpdateDestroyView.as_view(), name='edit_language'),
    path('edit/subgenre/<int:pk>/', SubGenresRetriveUpdateDestroyView.as_view(), name='edit_subgenre'),
    path('edit/book/<int:pk>/', BookRetriveUpdateDestroyView.as_view(), name='edit_book'),
    path('edit/review/<int:pk>/', BookReviewRetriveUpdateDestroyView.as_view(), name='edit_review'),
    
    path('list/book/', BooksListApiView.as_view(), name='list_book'),
    path('list/audiobook/', AudioBooksListApiView.as_view(), name='list_audiobook'),
    path('list/readbook/', ReadBooksListApiView.as_view(), name='list_readbook'),
    path('list/kidsbook/', KidsBooksListApiView.as_view(), name='list_kidsbook'),
    path('list/author/', AuthorListApiView.as_view(), name='list_author'),
    path('list/agelimit/', AgeLimitListApiView.as_view(), name='list_agelimit'),
    path('list/genre/', GenresListApiView.as_view(), name='list_genre'),
    path('list/language/', LanguageListApiView.as_view(), name='list_language'),
    path('list/subgenre/', SubGenresListApiView.as_view(), name='list_subgenre'),
    
    # Filters
    path('audio/<str:types>/<str:name>/', AudioBookFilterApiView.as_view()),
    path('read/<str:types>/<str:name>/', ReadBookFilterApiView.as_view()),
    path('kids/<str:types>/<str:name>/', KidsBookFilterApiView.as_view()),
    path('open/<int:id>/', ReadAndListenBookApiView.as_view()),
    path('filter/<str:type>/', BookFilterApiView.as_view(), name='book-filter'),
    path('counts/', AllCountsApiView.as_view(), name='counts'),
    
    
    path('search/', SearchBookApiView.as_view(), name='search_book'),
    
    path('', InfoPageView.as_view(), name='Info page')
]