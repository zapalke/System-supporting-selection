from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Field_of_Study(models.Model):
    DEGREES = (
        ('Licencjat', 'Licencjat'),
        ('Inżynier', 'Inżynier'),
        ('Magister', 'Magister'),
        ('Jednolite', 'Jednolite')
    )
    STUDY_MODE = (
        ('Stacjonarne','Stacjonarne'),
        ('Niestacjonarne', 'Niestacjonarne'),
        ('Stacjonarne i niestacjonarne', 'Stacjonarne i niestacjonarne')
    )
    name = models.CharField(max_length=100, default='Nieznane studia')                      # Nazwa kierunku studiów
    degree = models.CharField(max_length=20, choices=DEGREES)                               # Stopień studiów określony w zmiennej DEGREES
    study_mode = models.CharField(max_length=30, choices=STUDY_MODE)                        # Tryb studiów określony w zmiennej STUDY_MODE
    language = models.CharField(max_length=20,default='Polski')                             # Język studiów
    university = models.ForeignKey("University", on_delete=models.CASCADE, to_field='id')   # Klucz obcy do tabeli University, określa uczelnię na której odbywają się studia
    description = models.TextField(max_length=1000)                                         # Opis kierunku studiów
    link_to_site = models.CharField(max_length=255, default='Brak linku do strony')         # Link do strony kierunku studiów

    def save(self, *args, **kwargs):
        # Funkcja zapisująca obiekt do bazy danych.
        super().save(*args, **kwargs)

    class Meta:
        # Klasa Meta określająca nazwę tabeli w bazie danych.
        verbose_name_plural = 'Field of Studies'

    def __str__(self):
        # Funkcja zwracająca jak ma być wyświetlany obiekt w panelu administratora.
        return f'{self.name} - {self.university.name}'    


class University(models.Model):
    TYPES = (
        ('Uniwersytet','Uniwersytet'),
        ('Akademia Wychowania Fizycznego','Akademia Wychowania Fizycznego'),
        ('Uczelnia Ekonomiczna','Uczelnia Ekonomiczna'),
        ('Uczelnia Pedagogiczna','Uczelnia Pedagogiczna'),
        ('Uczelnia Przyrodniczo-Rolnicza','Uczelnia Przyrodniczo-Rolnicza'),
        ('Uczelnia Techniczna','Uczelnia Techniczna')
    )
    name = models.CharField(max_length=200, default='Nieznany Uniwersytet')
    city = models.CharField(max_length=50, default='Nieznane Miasto')
    type = models.CharField(max_length=30, choices=TYPES)
    rank_overall = models.IntegerField(default=0)
    rank_in_type = models.IntegerField(default=0)
    link_to_site =  models.CharField(max_length=255, default='Brak linku do strony')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Universities'

    def __str__(self):
        return f'{self.name}'   

class RoomPrice(models.Model):
    city = models.ForeignKey('University', on_delete=models.CASCADE, to_field='id')
    avg_room_price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Room Prices'

    def __str__(self):
        return f'{self.city}'       
    

class Subjects(models.Model):
    subject = models.CharField(max_length=80, default='Nieznany Przedmiot')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f'{self.subject}'  

class Exam_Subjects(models.Model):
    field_of_study = models.ForeignKey('Field_of_Study', on_delete=models.CASCADE, to_field='id')
    subject = models.ForeignKey('Subjects',on_delete=models.CASCADE, to_field='id')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Exam Subjects'

    def __str__(self):
        return f'{self.field_of_study} - {self.subject}'  
    
class Alternative_Exam_Subjects(models.Model):
    main_subject = models.ForeignKey('Exam_Subjects', on_delete=models.CASCADE, to_field='id')
    subject = models.ForeignKey('Subjects',on_delete=models.CASCADE, to_field='id')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Alternative Exam Subjects'

    def __str__(self):
        return f'{self.subject}'  
    
class Attributes(models.Model):
    attribute = models.CharField(max_length=120, default='Nieznana cecha')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return f'{self.attribute}'  

class Characteristics(models.Model):
    field_of_study = models.ForeignKey('Field_of_Study', on_delete=models.CASCADE, to_field='id')
    attribute = models.ForeignKey('Attributes',on_delete=models.CASCADE, to_field='id')
    fit = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Characteristics'

    def __str__(self):
        return f'{self.field_of_study} - {self.attribute}'  




