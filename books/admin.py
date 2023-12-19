from django.contrib import admin
from accounts.models import BookReview
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


admin.site.register(Author)
admin.site.register(AgeLimit)
admin.site.register(Genres)
admin.site.register(SubGenres)
admin.site.register(Language)
admin.site.register(Books)
admin.site.register(AudioFile)
admin.site.register(ReadFile)
admin.site.register(Links)
admin.site.register(BookReview)
