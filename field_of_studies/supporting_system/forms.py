from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import (Field_of_Study, University, Subjects, Exam_Subjects, 
                     Alternative_Exam_Subjects, Attribiutes, Characteristics)

from django.core.exceptions import ValidationError


class AddUniversityForm(forms.ModelForm):
    TYPES = (
        ('Uniwersytet','Uniwersytet'),
        ('Akademia Wychowania Fizycznego','Akademia Wychowania Fizycznego'),
        ('Uczelnia Ekonomiczna','Uczelnia Ekonomiczna'),
        ('Uczelnia Pedagogiczna','Uczelnia Pedagogiczna'),
        ('Uczelnia Przyrodniczo-Rolnicza','Uczelnia Przyrodniczo-Rolnicza'),
        ('Uczelnia Techniczna','Uczelnia Techniczna')
    )
    name = forms.CharField(max_length=200,required=True)
    city = forms.CharField(max_length=50,required=True)
    type = forms.ChoiceField(choices=TYPES,required=True)
    rank_in_type = forms.IntegerField(required=True)
    rank_overall = forms.IntegerField(required=True)
    link_to_site = forms.CharField(max_length=255,required=True)

    class Meta:
        model = University
        fields = ('name','city','type','rank_in_type','rank_overall','link_to_site')

    def clean_module(self):
        if self.cleaned_data['name'] in University.objects.values_list('name',flat=True):
            raise ValidationError(self.fields['name'].error_messages['invalid'])
        
    def __init__(self, *args, **kwargs):
        super(AddUniversityForm, self).__init__(*args, **kwargs)