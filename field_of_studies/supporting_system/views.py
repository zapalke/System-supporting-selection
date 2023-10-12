from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (ListView, TemplateView, FormView)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import AddUniversityForm, AddFieldForm, ExamSubjectForm, AlternativeExamSubjectForm, CharacteristicsForm
from .models import (Field_of_Study, University, Subjects,Exam_Subjects, 
                     Alternative_Exam_Subjects, Attributes, Characteristics)


class MainPageView(TemplateView):
    template_name = 'supporting_system/main_page.html'

class AddUniversityView(LoginRequiredMixin,FormView):
    def get(self, request):
        form_class = AddUniversityForm
        context = {'form':form_class}
        return render(request, 'supporting_system/add_university_view.html',context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        city = request.POST['city']
        type = request.POST['type']
        rank_overall = request.POST['rank_overall']
        rank_in_type = request.POST['rank_in_type']
        link_to_site = request.POST['link_to_site']
        uni_data = {
                    'name':name, 'city':city, 'type':type,'rank_overall':rank_overall,
                    'rank_in_type':rank_in_type, 'link_to_site':link_to_site
                }
        if name in University.objects.values_list('name',flat=True):
            context = {
                'obj':University.objects.get(name=name),
                'new_obj': uni_data
            }
            return render(request,'supporting_system/add_error.html',context)
        
        else:
            University.objects.create(**uni_data)

            if 'another' in request.POST:
                return HttpResponseRedirect(reverse('AddUniversityView'))
            else:
                return HttpResponseRedirect(reverse('ListUniversityView'))

class AddFieldView(LoginRequiredMixin, FormView):
    template_name = 'supporting_system/add_field_view.html'
    form_class = AddFieldForm
    
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        degree = request.POST['degree']
        study_mode = request.POST['study_mode']
        language = request.POST['language']
        university = request.POST['university']
        link_to_site = request.POST['link_to_site']
        description = request.POST['description']

        field_data = {
                    'name':name, 'degree':degree, 'study_mode':study_mode,'language':language,
                    'university':University.objects.get(id=university), 'link_to_site':link_to_site,
                    'description':description
                }
        try:
            existing_field = Field_of_Study.objects.get(
                name=name, degree=degree, study_mode=study_mode,
                language=language, university=university
                )
            context = {'obj':existing_field, 'new_obj':field_data}
            return render(request,'supporting_system/add_error.html',context)
        except Field_of_Study.DoesNotExist:
            obj = Field_of_Study.objects.create(**field_data)

            if 'another' in request.POST:
                return HttpResponseRedirect(reverse('AddFieldView'))
            elif 'subject' in request.POST:
                return HttpResponseRedirect(reverse('AddSubjectsToFieldView',kwargs={'field_of_study_id':obj.id}))
            elif 'characteristics' in request.POST:
                return HttpResponseRedirect(reverse('AddCharacteristicsView',kwargs={'field_of_study_id':obj.id}))
            else:
                return HttpResponseRedirect(reverse('ListFieldView')) 

class AddSubjectsToFieldView(LoginRequiredMixin, FormView):
    template_name = 'supporting_system/add_subject_view.html'
    form_class = ExamSubjectForm
    
    def get_initial(self):
        initial = super().get_initial()

        field_of_study_id = self.kwargs.get('field_of_study_id')
        if field_of_study_id:
            try:
                field_of_study = Field_of_Study.objects.get(id=field_of_study_id)
                initial['field_of_study'] = field_of_study
            except Field_of_Study.DoesNotExist:
                pass  

        return initial
    
    def post(self, request, *args, **kwargs):
        field_of_study = Field_of_Study.objects.get(id=self.kwargs.get('field_of_study_id'))
        subject = Subjects.objects.get(id=request.POST['subject'])

        if subject.subject != '0Nieznany Przedmiot':
            field_data = {
                        'field_of_study':field_of_study, 'subject':subject
                    }
            try:
                existing_field = Exam_Subjects.objects.get(
                    field_of_study=field_of_study, subject=subject
                    )
                context = {'obj':existing_field, 'new_obj':field_data}
                return render(request,'supporting_system/add_error.html',context)
            except Exam_Subjects.DoesNotExist:
                obj = Exam_Subjects.objects.create(**field_data)

        if 'another' in request.POST:
            return HttpResponseRedirect(reverse('AddSubjectsToFieldView', kwargs={'field_of_study_id':field_of_study.id}))
        elif 'alternative' in request.POST:
            return HttpResponseRedirect(reverse('AddAlternativeSubjectsToFieldView', kwargs={'main_subject_id':obj.id}))
        elif 'field' in request.POST:
            return HttpResponseRedirect(reverse('AddFieldView'))
        elif 'characteristics' in request.POST:
            return HttpResponseRedirect(reverse('AddCharacteristicsView',kwargs={'field_of_study_id':field_of_study.id}))
        else:
            return HttpResponseRedirect(reverse('ListFieldView'))  

class AddAlternativeSubjectsToFieldView(LoginRequiredMixin, FormView):
    template_name = 'supporting_system/add_alternative_subject_view.html'
    form_class = AlternativeExamSubjectForm
    
    def get_initial(self):
        initial = super().get_initial()

        main_subject_id = self.kwargs.get('main_subject_id')
        if main_subject_id:
            try:
                main_subject = Exam_Subjects.objects.get(id=main_subject_id)
                initial['main_subject'] = main_subject
            except Exam_Subjects.DoesNotExist:
                initial['main_subject'] = 0 

        return initial
    
    def post(self, request, *args, **kwargs):
        main_subject = Exam_Subjects.objects.get(id=self.kwargs.get('main_subject_id'))

        print(request.POST.getlist('subjects'))
        for single_subject in request.POST.getlist('subjects'):
            subject = Subjects.objects.get(id=single_subject)
            if subject.subject != '0Nieznany Przedmiot':
                field_data = {
                        'main_subject':main_subject, 'subject':subject
                        }
                try:
                    existing_field = Alternative_Exam_Subjects.objects.get(
                        main_subject=main_subject, subject=subject
                        )
                    context = {'obj':existing_field, 'new_obj':field_data}
                    return render(request,'supporting_system/add_error.html',context)
                except Alternative_Exam_Subjects.DoesNotExist:
                    Alternative_Exam_Subjects.objects.create(**field_data)

        if 'another' in request.POST:
            return HttpResponseRedirect(reverse('AddAlternativeSubjectsToFieldView', kwargs={'main_subject_id':main_subject.id}))
        elif 'main' in request.POST:
            return HttpResponseRedirect(reverse('AddSubjectsToFieldView',kwargs={'field_of_study_id':main_subject.field_of_study.id}))
        elif 'field' in request.POST:
            return HttpResponseRedirect(reverse('AddFieldView'))
        elif 'characteristics' in request.POST:
            return HttpResponseRedirect(reverse('AddCharacteristicsView',kwargs={'field_of_study_id':main_subject.field_of_study.id}))
        else:
            return HttpResponseRedirect(reverse('ListFieldView'))    

class AddCharacteristicsView(FormView):
    template_name = 'supporting_system/add_characteristics_view.html'
    form_class = CharacteristicsForm

    def get_initial(self):
        initial = super().get_initial()

        field_of_study_id = self.kwargs.get('field_of_study_id')
        if field_of_study_id:
            try:
                field_of_study = Field_of_Study.objects.get(id=field_of_study_id)
                initial['field_of_study'] = field_of_study
            except Field_of_Study.DoesNotExist:
                pass  

        return initial

    def post(self, request, *args, **kwargs):
        field_of_study = Field_of_Study.objects.get(id=self.kwargs.get('field_of_study_id'))

        attribute = Attributes.objects.get(id=request.POST['attributes'])
        fit = request.POST['fit']
        if attribute.attribute != '0Nieznana cecha':
            field_data = {
                        'field_of_study':field_of_study, 'attribute':attribute,
                        'fit':fit
                    }
            try:
                existing_field = Characteristics.objects.get(
                    field_of_study=field_of_study, attribute=attribute,
                )
                context = {'obj':existing_field, 'new_obj':field_data}
                return render(request,'supporting_system/add_error.html',context)
            except Characteristics.DoesNotExist:
                Characteristics.objects.create(**field_data)

        if 'another' in request.POST:
            return HttpResponseRedirect(reverse('AddCharacteristicsView',kwargs={'field_of_study_id':field_of_study.id}))
        elif 'field' in request.POST:
            return HttpResponseRedirect(reverse('AddFieldView'))
        elif 'main' in request.POST:
            return HttpResponseRedirect(reverse('AddSubjectsToFieldView',kwargs={'field_of_study_id':field_of_study.id}))
        else:
            return HttpResponseRedirect(reverse('ListFieldView'))  

    