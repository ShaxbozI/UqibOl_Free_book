from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse



class InfoPageView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, *args, **kwargs):
        response = {
            'Info': "Barcha API url manzillarni shu yerda!",
                
            "Ro'yhatdan o'tish va Shaxsiy hisob": {
                "Ro'yhatdan o'tish": reverse('singup'),
                "Kodni tasdiqlash": reverse('verify'),
                "Yangi kod olish": reverse('new_verify'),
                "Hisob malumotlarini kiritish yoki yangilash": reverse('change_info'),
                "Hisob uchun foto yuklash": reverse('change_photo'),
                
                "Hisobga kirish": reverse('login'),
                "Refresh tokenni yangilash": reverse('login_refresh'),
                "Hisobdan chiqish": reverse('logout'),
                "Maxfiy so'zni yangilash so'rovi": reverse('forgot_password'),
                "Maxfiy so'zni yangilash": reverse('resset_password')
            },
            
            "Malumotlar kiritish(yaratish)": {
                "Muallif": reverse('add_author'),
                "Yosh chegarasi": reverse('add_agelimit'),
                "Janr": reverse('add_genre'),
                "Ichki janr": reverse('add_subgenre'),
                "Til": reverse('add_language'),
                "Kitob": reverse('add_book'),
                "Izoh": reverse('add_review'),
            },
            
            "Malumotlar yangilash(o'zgartirish) va o'chirish": {
                "Muallif": "/edit/author/'malimot id raqami'/",
                "Yosh chegarasi": "/edit/agelimit/'malimot id raqami'/",
                "Janr": "/edit/genre/'malimot id raqami'/",
                "Ichki janr": "/edit/subgenre/'malimot id raqami'/",
                "Til": "/edit/language/'malimot id raqami'/",
                "Kitob": "/edit/book/'malimot id raqami'/",
                "Izoh": "/edit/review/'malimot id raqami'/",
            },
            
            "Umumiy malumotlarni olish": {
                "Muallif": reverse('list_author'),
                "Yosh chegarasi": reverse('list_agelimit'),
                "Janr": reverse('list_genre'),
                "Ichki janr": reverse('list_subgenre'),
                "Til": reverse('list_language'),
                "Kitob": reverse('list_book'),
                "Kitob Audio faylli": reverse('list_audiobook'),
                "Kitob o'qish mumkin bo'lgan": reverse('list_readbook'),
                "Bolalar Kitoblari": reverse('list_kidsbook'),
            },
            
            "Filterllangan malumotlar": {
                "Audio kitoblarni filterlash": {
                        "umumiy url": "/audio/<str:types>/<str:name>/",
                        "Tillar bo'yicha": "/audio/language/'til nomi'/",
                        "Janrlar bo'yicha": "/audio/genre/'janr nomi'/"
                    },
                "O'riladigan kitoblarni filterlash": {
                        "umumiy url": "/read/<str:types>/<str:name>/",
                        "Tillar bo'yicha": "/read/language/'til nomi'/",
                        "Janrlar bo'yicha": "/read/genre/'janr nomi'/"
                    },
                "Bolalar kitoblarni filterlash": {
                        "umumiy url": "/kids/<str:types>/<str:name>/",
                        "Tillar bo'yicha": "/kids/language/'til nomi'/",
                        "Janrlar bo'yicha": "/kids/genre/'janr nomi'/"
                    },
                
                "Ayni bir kitobni olish va o'qish/eshitish uchun izohlari bilan birga": "open/<int:id>/",
                
                "Malumotlar Jamlangan holatdagi filterlar": {
                    'Pastdagi Barcha filterlar birga jamlang holatda': reverse('book-filter', kwargs={'type': 'all'}),
                    
                    "Sahifalash imkoniyati mavjud": {
                        'Barcha kitoblar': reverse('book-filter', kwargs={'type': 'books'}),
                        "Faqat o'qish mumkin bo'lgan": reverse('book-filter', kwargs={'type': 'readbooks'}),
                        "Faqat tinglash mumkin bolgan": reverse('book-filter', kwargs={'type': 'audiobooks'}),
                        "Eng ko'p o'qilganlar": reverse('book-filter', kwargs={'type': 'read_alot'}),
                        "Eng ko'p eshitishlar": reverse('book-filter', kwargs={'type': 'listen_alot'}),
                        "Bolalar uchun": reverse('book-filter', kwargs={'type': 'child_books'}),
                    }
                }
            },
           
            "Kitoblar qidiruvi":  f"{reverse('search_book')}?q='qidruv nomi'",
            "Malumotlar sanog'i":  "/counts/"
        }
        
        return Response(response, status=status.HTTP_200_OK)