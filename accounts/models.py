from datetime import datetime, timedelta
from django.utils import timezone
import random
import uuid
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from utility.models import BaseModel
from books.models import Books


from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import FileExtensionValidator


USER, ADMIN, SUPER_ADMIN = ('user', 'admin', 'super_admin')
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')



class User(AbstractUser, BaseModel):
    
    USER_ROLES = ( 
        (USER, USER),
        (ADMIN, ADMIN),
        (SUPER_ADMIN, SUPER_ADMIN)
    )
    
    AUTH_TYPE = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    
    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True,
        validators = [FileExtensionValidator(allowed_extensions = ['jpg', 'png', 'jpeg'])]
    )
    read_books = models.ManyToManyField(Books)
    
    def __str__(self): 
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def create_verify_code(self, verify_type):
        code = ''.join([str(random.randint(0, 100)%10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id = self.id,
            verify_type = verify_type,
            code = code
        )
        return code
        
    def check_username(self):
        if not self.username:
            temp_username = f"user-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username = temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username
            
    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            existing_user = User.objects.filter(email=normalize_email).exclude(id=self.id).first()
            if existing_user:
                raise ValidationError({'email': 'Bu email allaqachon foydalanilmoqda'})
    
    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
            
    def token(self):
        refresh = RefreshToken.for_user(self)
        return{
            'access': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
    
    
    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)
        
    def clean(self):
        self.check_email()
        self.check_pass()
        self.hashing_password()
        self.check_username()
    
    
    
    
    
EMAIL_EXPIRE = 5
PHONE_EXPIRE = 2

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    code = models.CharField(max_length=4, unique=True)
    user = models.ForeignKey('accounts.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.__str__())
    
    def save(self, *args, **kwargs):
        if self.verify_type==VIA_EMAIL:
            self.expiration_time=datetime.now() + timedelta(minutes = EMAIL_EXPIRE)
        else:
            self.expiration_time=datetime.now() + timedelta(minutes = PHONE_EXPIRE)
            
        super(UserConfirmation, self).save(*args, **kwargs)
    





class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    stars_given = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.book.title} : {self.user.username} || {self.stars_given}"