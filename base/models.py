from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=128, null=True)

class Book(models.Model):
    title = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=2000, null=True)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)



class Member(Person):
    registration_date = models.DateField(null=True)



class Author(models.Model):
    age = models.IntegerField(null=True)


class Borrow(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.member.name + " " + self.book.title + " " + str(self.date)




class Reservation(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)

    