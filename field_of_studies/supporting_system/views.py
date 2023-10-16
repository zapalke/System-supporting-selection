from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (ListView, TemplateView, FormView)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import (AddUniversityForm, AddFieldForm, ExamSubjectForm, FieldFilterForm,
                    AlternativeExamSubjectForm, CharacteristicsForm)
from .models import (Field_of_Study, University, Subjects,Exam_Subjects, 
                     Alternative_Exam_Subjects, Attributes, Characteristics)
from collections import defaultdict


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
                return HttpResponseRedirect(reverse('FieldListView')) 

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
            return HttpResponseRedirect(reverse('FieldListView'))  

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
            return HttpResponseRedirect(reverse('FieldListView'))    

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
            return HttpResponseRedirect(reverse('FieldListView'))  

def filter_by_subjects(queryset, subjects):
    allowed_id = []
    for field in queryset:
        exam_subjects_for_field = Exam_Subjects.objects.filter(field_of_study=field.id).all()
        exam_subjects_for_field_checklist = []
        for sub in exam_subjects_for_field:
            if str(sub.subject.id) in subjects:
                exam_subjects_for_field_checklist.append(1)
            else:
                alternative_exam_subjects_for_field = Alternative_Exam_Subjects.objects.filter(main_subject=sub.id).all()
                for alternative_subject in alternative_exam_subjects_for_field:
                    if str(alternative_subject.subject.id) in subjects:
                        exam_subjects_for_field_checklist.append(1)
                        break
        if len(exam_subjects_for_field_checklist) == exam_subjects_for_field.count():
            allowed_id.append(field.id)
    return allowed_id
                
                

def FieldView(request):
    queryset = Field_of_Study.objects.all().order_by('name')
    if 'clear' in request.GET:
        return HttpResponseRedirect(reverse('FieldListView'))  
    else:
        degree = request.GET.getlist('degree')
        if degree != []:
            to_filter = []
            if 'I Stopień' in degree:
                to_filter.append('Licencjat')
                to_filter.append('Inżynier')
                to_filter.append('Jednolite')
            if 'II Stopień' in degree:
                to_filter.append('Magister')
            queryset = queryset.filter(degree__in=to_filter)
        university = request.GET.getlist('university')
        if university != []:
            queryset = queryset.filter(university__in=university)
        language = request.GET.getlist('language')
        if language != []:
            queryset = queryset.filter(language__in=language)
        city = request.GET.getlist('city')
        if city != []:
            queryset = queryset.filter(university__city__in=city)
        study_mode = request.GET.getlist('study_mode')
        if study_mode != []:
            if len(study_mode) == 2:
                study_mode.append('Stacjonarne i niestacjonarne')
            queryset = queryset.filter(study_mode__in=study_mode)
        subjects = request.GET.getlist('subjects')
        if subjects != []:
            allowed_fields = filter_by_subjects(queryset,subjects)
            queryset = queryset.filter(id__in=allowed_fields)
    
    paginator = Paginator(queryset, 15)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    initials = {
        'degree':degree,'university':university,'subjects':subjects,
        'language':language, 'city':city, 'study_mode':study_mode
        }
    context = {
        'form':FieldFilterForm(initial=initials),
        'fields':response,
        'initials':initials
        
    }
    return render(request, 'supporting_system/fields_list_view.html', context)

def DiscoverView_degree(request):
    degrees = ['I Stopień', 'II Stopień']
    if request.method == 'GET':
        context = {
            'degree': degrees
        }
        return render(request, 'supporting_system/discover_degree_view.html', context)
    else:
        degree = request.POST.get('degree')
        if degree == degrees[0]:
            request.session['filtered_fields'] = list(Field_of_Study.objects.filter(degree__in=['Licencjat','Inżynier','Jednolite']).values_list('id',flat=True))
            return HttpResponseRedirect(reverse('DiscoverView_subjects'))
        else:
            request.session['filtered_fields'] = list(Field_of_Study.objects.filter(degree='Magister').values_list('id',flat=True))
            return HttpResponseRedirect(reverse('DiscoverView_main'))
        
    
def DiscoverView_subjects(request):
    if request.method == 'GET':
        context = {
            'subjects': Subjects.objects.exclude(subject='0Nieznany Przedmiot').all()
        }
        return render(request, 'supporting_system/discover_subjects_view.html', context)
    else:
        if request.POST.getlist('subjects'):
            fields_matching_subjects = filter_by_subjects(
                Field_of_Study.objects.filter(id__in=request.session['filtered_fields']).all(),
                request.POST.getlist('subjects')
                )
            request.session['filtered_fields'] = fields_matching_subjects
        return HttpResponseRedirect(reverse('DiscoverView_main'))
    
def get_attributes_to_display(approved_attrs, excluded_attrs,filtered_fields):
    fields_with_approved_attrs = Characteristics.objects.filter(attribute__in=approved_attrs, field_of_study__in=filtered_fields).values_list('field_of_study',flat=True)
    prefered_attrs = list(Characteristics.objects.filter(field_of_study__in=fields_with_approved_attrs).exclude(attribute__in=excluded_attrs).exclude(attribute__in=approved_attrs).order_by('?').values_list('attribute__id',flat=True))
    prefered_attrs = list(dict.fromkeys(prefered_attrs))
    other_attrs = list(Characteristics.objects.exclude(attribute__in=prefered_attrs).exclude(attribute__in=approved_attrs).exclude(attribute__in=excluded_attrs).order_by('?').values_list('attribute__id',flat=True))
    other_attrs = list(dict.fromkeys(other_attrs))
    print(f'Found {len(prefered_attrs)} prefered attrs and {len(other_attrs)} other')
    
    attrs_to_display = []
    proportion = 0.8
    len_of_attrs = 10
    added_other = 0
    added_prefered = 0
    for i in range(len_of_attrs):
        if added_prefered < int(len_of_attrs*proportion):
            if len(prefered_attrs) > 0:
                attrs_to_display.append(prefered_attrs[0])
                prefered_attrs.pop(0)
                added_prefered += 1
            elif len(other_attrs) > 0:
                attrs_to_display.append(other_attrs[0])
                other_attrs.pop(0)
                added_other += 1

        elif added_other < int(len_of_attrs*proportion):
            if len(other_attrs) > 0:
                attrs_to_display.append(other_attrs[0])
                other_attrs.pop(0)
                added_other += 1
            elif len(prefered_attrs) > 0:
                attrs_to_display.append(prefered_attrs[0])
                prefered_attrs.pop(0)
                added_prefered += 1
    print(f'{attrs_to_display} will be displayed with {added_prefered} prefered attrs and {added_other} other attrs.')
    return attrs_to_display, added_prefered

def DiscoverView(request):
    approved_attributes = request.POST.getlist('approved')
    excluded_attributes = request.POST.getlist('all')
    if approved_attributes == [] and excluded_attributes == []:
        print('Clearing data')
        request.session['discover_try'] = 0
        request.session['approved_attributes'] = []
        request.session['excluded_attributes'] = []
    else:
        request.session['approved_attributes'].extend(approved_attributes)
        excluded_attributes = [x for x in excluded_attributes if x not in approved_attributes]
        request.session['excluded_attributes'].extend(excluded_attributes)
        request.session['discover_try'] += 1
        request.session.modified=True

    attrs_to_display, added_prefered = get_attributes_to_display(
        request.session['approved_attributes'],request.session['excluded_attributes'], 
        request.session['filtered_fields']
        )
    max_tries = 5
    if request.session['discover_try'] < max_tries and len(attrs_to_display) != 0:
    #if len(attrs_to_display) != 0:
        print(request.session['approved_attributes'], request.session['excluded_attributes'])
        context = {
            'attrs':Attributes.objects.filter(id__in=attrs_to_display).all(),
            'progress': round(request.session['discover_try']/max_tries,2)*100
        }
        return render(request, 'supporting_system/discover_view.html', context)
    else:
        return HttpResponseRedirect(reverse('DiscoverView_results'))

def DiscoverResultsView(request):
    results_of_fields = defaultdict(float)
    characteristics = Characteristics.objects.filter(
        field_of_study__in=request.session['filtered_fields'], 
        attribute__in=request.session['approved_attributes']
        ).all()
    
    for char in characteristics:
        results_of_fields[char.field_of_study.id] += char.fit
    
    #Other version of algorythm using percentage of sum of all characteristics)
    shown_characteristics = request.session['approved_attributes']
    shown_characteristics.extend(request.session['excluded_attributes'])

    for key, value in results_of_fields.items():
        chars = list(Characteristics.objects.filter(field_of_study=key, attribute__id__in=shown_characteristics).values_list('fit',flat=True))
        results_of_fields[key] = (value*100)/sum(chars)
        print(f'{key} - {results_of_fields[key]} ({len(chars)}/{Characteristics.objects.filter(field_of_study=key).values_list("fit",flat=True).count()}) - {Field_of_Study.objects.get(id=key)}')

    # del request.session['discover_try']
    # del request.session['approved_attributes']
    # del request.session['excluded_attributes']
    # del request.session['filtered_fields']

    results_of_fields = dict(sorted(results_of_fields.items(), key=lambda x: x[1],reverse=True))
    results_top3 = []
    results_rest = []
    for key, value in results_of_fields.items():
        if len(results_top3) < 3:
            results_top3.append([Field_of_Study.objects.get(id=key), round(value,2), Characteristics.objects.filter(field_of_study=key, attribute__id__in=shown_characteristics).count(),Characteristics.objects.filter(field_of_study=key).count()])
        elif value >= 25.0 and len(results_rest) < 10:
            results_rest.append([Field_of_Study.objects.get(id=key), round(value,2), Characteristics.objects.filter(field_of_study=key, attribute__id__in=shown_characteristics).count(),Characteristics.objects.filter(field_of_study=key).count()])
        else:
            break
        
    context = {
            'results_top3':results_top3,
            'results_rest':results_rest,
        }
    return render(request, 'supporting_system/discover_results_view.html', context)

# def DiscoverResultsView(request):
#     results_of_fields = defaultdict(float)
#     try:
#         print('Subjects: ',request.session['subjects'])
#         filtered_fields = filter_by_subjects(
#             Field_of_Study.objects.filter(degree__in=request.session['degree']).all(),
#             request.session['subjects']
#             )
#         print(filtered_fields)
#     except KeyError:
#         print('Key error')
#         filtered_fields = Field_of_Study.objects.filter()
#     characteristics = Characteristics.objects.filter(
#         field_of_study__in=filtered_fields, attribute__in=request.session['approved_attributes']
#         ).all()
    
#     for char in characteristics:
#         results_of_fields[char.field_of_study.id] += char.fit

#     # del request.session['discover_try']
#     # del request.session['approved_attributes']
#     # del request.session['excluded_attributes']
#     # del request.session['subjects']
#     # del request.session['degree']

#     results_of_fields = dict(sorted(results_of_fields.items(), key=lambda x: x[1],reverse=True))
#     results_top3 = []
#     results_rest = []
#     for key, value in results_of_fields.items():
#         if len(results_top3) < 3:
#             results_top3.append(Field_of_Study.objects.get(id=key))
#         elif value >= 1.0 and len(results_rest) < 10:
#             results_rest.append(Field_of_Study.objects.get(id=key))
#         else:
#             break

#     for key,value in results_of_fields.items():
#         print(f'{key} - {value} - {Field_of_Study.objects.get(id=key)}')
#     context = {
#             'results_top3':results_top3,
#             'results_rest':results_rest
#         }
#     return render(request, 'supporting_system/discover_results_view.html', context)

