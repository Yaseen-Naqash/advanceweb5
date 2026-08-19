from django.contrib import admin
from .models import Book, Member, Author, Borrow, Reservation

# Register your models here.
admin.site.register(Book)
admin.site.register(Member)

admin.site.register(Author)
admin.site.register(Borrow)
admin.site.register(Reservation)