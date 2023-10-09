from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import (Field_of_Study, University, Subjects, Exam_Subjects, 
                     Alternative_Exam_Subjects, Attributes, Characteristics)

from django.core.exceptions import ValidationError


class AddUniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ('name','city','type','rank_in_type','rank_overall','link_to_site')

    def clean_module(self):
        if self.cleaned_data['name'] in University.objects.values_list('name',flat=True):
            raise ValidationError(self.fields['name'].error_messages['invalid'])
        
    def __init__(self, *args, **kwargs):
        super(AddUniversityForm, self).__init__(*args, **kwargs)

class AddFieldForm(forms.ModelForm):
    class Meta:
        model = Field_of_Study
        fields = ('name','degree', 'study_mode', 'language','university','link_to_site','description')

    def clean_module(self):
        if self.cleaned_data['name'] in Field_of_Study.objects.values_list('name',flat=True):
            raise ValidationError(self.fields['name'].error_messages['invalid'])
        
    def __init__(self, *args, **kwargs):
        super(AddFieldForm, self).__init__(*args, **kwargs)

class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = Exam_Subjects
        fields = ['field_of_study','subject']

class AlternativeExamSubjectForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subjects.objects.all().order_by('-subject'),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Alternative_Exam_Subjects
        fields = ['main_subject', 'subject']

class CharacteristicsForm(forms.ModelForm):
    attributes = forms.ModelChoiceField(
        queryset=Attributes.objects.all().order_by('attribute'),
        )

    fit = forms.FloatField(
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.2', 'min': '0.0', 'max': '1.0'}),)
    class Meta:
        model = Characteristics
        fields = ['field_of_study','attribute', 'fit']

    def clean_fit(self):
        fit = self.cleaned_data.get('fit')
        if fit is not None and (fit < 0.0 or fit > 1.0):
            raise forms.ValidationError("Fit value must be between 0.0 and 1.0.")
        return fit