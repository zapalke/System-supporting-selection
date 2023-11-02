from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (ListView, TemplateView, FormView)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import ( AddFieldForm, ExamSubjectForm, FieldFilterForm,
                    AlternativeExamSubjectForm, CharacteristicsForm)
from .models import (Field_of_Study, University, Subjects,Exam_Subjects, 
                     Alternative_Exam_Subjects, Attributes, Characteristics,
                     RoomPrice)
from collections import defaultdict, Counter


class MainPageView(TemplateView):
    """Template View for main page which contains links for subpages
    """
    template_name = 'supporting_system/main_page.html'

class AboutView(TemplateView):
    """Template view for About page which contains some information about the project
    """
    template_name = 'supporting_system/about_view.html'

class AddFieldView(LoginRequiredMixin, FormView):
    """View that helps with adding new study fields to database.
    The view is login protected so only logged in users can access it.
    
    Returns:
        There are several pages where page can redirect, based on button clicked in template.
        AddFieldView: Add another study field
        AddSubjectsToFieldView: Add exam subjects requried to qualify for given field
        AddCharacteristicsView: Add some attributes that describe given study field
        FieldListView: Page that lists all study fields in database
    """
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
        
        # Exception that checks if given field already exists in database
        # It field exists it displays error page
        try:
            existing_field = Field_of_Study.objects.get(
                name=name, degree=degree, study_mode=study_mode,
                language=language, university=university
                )
            context = {'obj':existing_field, 'new_obj':field_data}
            return render(request,'supporting_system/add_error.html',context)
        
        # If not it creates new object
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
    """View that helps with adding exam subjects required to qualify for given
    study field. The view is login protected so only logged in users can access it.
    
    Returns:
        There are several pages where page can redirect, based on button clicked in template.
        AddFieldView: Add another study field
        AddSubjectsToFieldView: Add exam subjects requried to qualify for given field
        AddAlternativeSubjectsToFieldView: Add subjects that can be an alternative to the current one
        AddCharacteristicsView: Add some attributes that describe given study field
        FieldListView: Page that lists all study fields in database
    """
    template_name = 'supporting_system/add_subject_view.html'
    form_class = ExamSubjectForm
    
    # Function that finds in url to which study field you want to add subjects
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

        # "0Nieznany przedmiot" acts like a dummy subject to exit page without adding anything
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
    """View that helps with adding alternative exam subjects to given subject.
    To qualify for some study field you sometimes can have for example Physics OR Computer Science, 
    this view will add CS as an alternative to Physics. 
    The view is login protected so only logged in users can access it.
    
    Returns:
        There are several pages where page can redirect, based on button clicked in template.
        AddFieldView: Add another study field
        AddSubjectsToFieldView: Add exam subjects requried to qualify for given field
        AddAlternativeSubjectsToFieldView: Add subjects that can be an alternative to the current one
        AddCharacteristicsView: Add some attributes that describe given study field
        FieldListView: Page that lists all study fields in database
    """
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

        #print(request.POST.getlist('subjects'))
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
    """View that helps with adding some attributes that describe given study field.
    These attributes are later used in DSS. The view is login protected so only logged in users can access it.
    
    Returns:
        There are several pages where page can redirect, based on button clicked in template.
        AddFieldView: Add another study field
        AddSubjectsToFieldView: Add exam subjects requried to qualify for given field
        AddCharacteristicsView: Add some attributes that describe given study field
        FieldListView: Page that lists all study fields in database
    """
    template_name = 'supporting_system/add_characteristics_view.html'
    form_class = CharacteristicsForm

    # Getting initial field of study to add attribute
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
        
        # "0Nieznana cecha" acts like dummy attribute to exit the form without adding anything
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
    """Function that filters study field based on exam subjects. It checks if subjects requried to qualify
    for a given field are in the list of passed subjects. If the so called main subject does not match anything
    function checks if there are some alternatives.

    Args:
        queryset (queryset): Field_of_Study model queryset to be filtered
        subjects (list): Subjects that user choosed 

    Returns:
        queryset: Filtered queryset
    """
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
    """View that lists all study fields. It also allows filtering the queryset by 
    some attributes like degree, univeristy or exam subjects. Whole page is limited to display 15
    elements
    """
    queryset = Field_of_Study.objects.all().order_by('name')
    
    # Simple method to clear the filters
    if 'clear' in request.GET:
        return HttpResponseRedirect(reverse('FieldListView'))  
    
    # Checking and applying filters that are in the get request
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

    # Initial elements that were choosed in filters
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

# Decission Supporting System based on candiate best fit (percentage of characteristics that were choosen by the user) for given field 

def DiscoverView_criteria(request):
    """The page that starts DSS. It asks user to choose what and how important are some criteria for him.
    It later stores the information in django sessions.

    Returns:
        DiscoverView_degree: Page which allows to choose which level of study fields is user looking for.
    """
    
    if request.method == 'GET':
        try:
            del request.session['discover_progress']
            del request.session['discover_try_attributes']
            del request.session['approved_attributes']
            del request.session['excluded_attributes']
            del request.session['filtered_fields']
        except KeyError:
            pass
        criteria = {
                    'city':'Miasto studiowania','uni':'Uniwersytet','uni_rank':'Ranking uczelni',
                    'characteristics':'Lubiane tematyki', 'living_expenses':'Koszty utrzymania'
            }
        request.session['discover_try_attributes'] = 5
        request.session['discover_progress'] = 0
        request.session['discover_max_pages'] = 5 + request.session['discover_try_attributes']

        context = {
            'criteria': criteria,
            'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
        }
        return render(request, 'supporting_system/discover_criteria_view.html', context)
    else:
        city_score, uni_score, uni_rank_score, characteristics_score, living_expenses_score = 0,0,0,0,0
        if request.POST.get('city'):
             city_score = int(request.POST.get('city'))
             if city_score == 0:
                 request.session['discover_max_pages'] -= 1
        if request.POST.get('uni'):
            uni_score = int(request.POST.get('uni'))
            if uni_score == 0:
                 request.session['discover_max_pages'] -= 1
        if request.POST.get('uni_rank'):
            uni_rank_score = int(request.POST.get('uni_rank'))
        if request.POST.get('characteristics'):
            characteristics_score = int(request.POST.get('characteristics'))
            if characteristics_score == 0:
                 request.session['discover_max_pages'] -= request.session['discover_try_attributes']
        if request.POST.get('living_expenses'):
            living_expenses_score = int(request.POST.get('living_expenses'))

        request.session['criteria'] = {
            'city':city_score,'uni':uni_score,'uni_rank':uni_rank_score,'characteristics':characteristics_score,
            'living_expenses':living_expenses_score
        }
        print(request.session)
        return HttpResponseRedirect(reverse('DiscoverView_degree'))

def DiscoverView_degree(request):
    """The first criterion of DSS. It asks user to choose which level of study fields is he looking for.
    Then it filters avielable study fields. This page uses django sessions to store information about the user

    Returns:
        DiscoverView_subjects: Page that allows user to choose which exam subjects did he take. It
        is only required for first degree study fields
        DiscoverView_main: Page which allows to choose attributes.
    """
    request.session['discover_progress'] += 1
    
    degrees = ['I Stopień', 'II Stopień']
    if request.method == 'GET':
        context = {
            'degree': degrees,
            'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
        }
        return render(request, 'supporting_system/discover_degree_view.html', context)
    else:
        degree = request.POST.get('degree')
        if degree == degrees[0]:
            request.session['filtered_fields'] = list(Field_of_Study.objects.filter(degree__in=['Licencjat','Inżynier','Jednolite']).values_list('id',flat=True))
            return HttpResponseRedirect(reverse('DiscoverView_subjects'))
        else:
            request.session['filtered_fields'] = list(Field_of_Study.objects.filter(degree='Magister').values_list('id',flat=True))
            request.session['discover_max_pages'] -= 1
            return HttpResponseRedirect(reverse('DiscoverView_cities'))
        
    
def DiscoverView_subjects(request):
    """The second criterion of DSS. It asks user to choose what subjects did he take at end of middle school.
    Knowing the subjects it filters queryset of avielable study fields and stores it in session.

    Returns:
        DiscoverView_cities: Page which allows to choose cities.
    """
    
    if request.method == 'GET':
        request.session['discover_progress'] += 1
        context = {
            'subjects': Subjects.objects.exclude(subject='0Nieznany Przedmiot').all(),
            'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
        }
        return render(request, 'supporting_system/discover_subjects_view.html', context)
    else:
        if request.POST.getlist('subjects'):
            fields_matching_subjects = filter_by_subjects(
                Field_of_Study.objects.filter(id__in=request.session['filtered_fields']).all(),
                request.POST.getlist('subjects')
                )
            request.session['filtered_fields'] = fields_matching_subjects
        return HttpResponseRedirect(reverse('DiscoverView_cities'))

def DiscoverView_cities(request):
    """The third criterion of DSS. It asks user to choose if he has any preferences regarding the city where 
    he would like to study. Note that this criteria does not work like a filter, at the end it will be added as 
    a metric to the overall study field score. List of cities is stored in session.

    Returns:
        DiscoverView_main: Page which allows to choose attributes.
    """
    if request.session['criteria']['city'] == 0:
        return HttpResponseRedirect(reverse('DiscoverView_uni'))
    
    if request.method == 'GET':
        request.session['discover_progress'] += 1
        context = {
            'cities': University.objects.values_list('city',flat=True).distinct(),
            'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
        }
        return render(request, 'supporting_system/discover_cities_view.html', context)
    else:
        if request.POST.getlist('cities'):
            request.session['cities'] = request.POST.getlist('cities')
        return HttpResponseRedirect(reverse('DiscoverView_uni'))
    
def DiscoverView_uni(request):
    """The fourth criterion of DSS. It asks user to choose if he has any preferences regarding the city where 
    he would like to study. Note that this criteria does not work like a filter, at the end it will be added as 
    a metric to the overall study field score. List of cities is stored in session.

    Returns:
        DiscoverView_main: Page which allows to choose attributes.
    """
    if request.session['criteria']['uni'] == 0:
        return HttpResponseRedirect(reverse('DiscoverView_main'))

    if request.method == 'GET':
        request.session['discover_progress'] += 1
        context = {
            'universities': University.objects.all(),
            'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
        }
        return render(request, 'supporting_system/discover_uni_view.html', context)
    else:
        if request.POST.getlist('university'):
            request.session['university'] = request.POST.getlist('university')
        return HttpResponseRedirect(reverse('DiscoverView_main'))

def get_attributes_to_display(approved_attrs, excluded_attrs,filtered_fields):
    """Funtion that creates a list of attributes to display for user in the next page.
    It's supposed to be semi random so that most of the attributes come from study fields which already have some 
    attributes approved by user.
    Args:
        approved_attrs (list): Contains attributes approbed by the user
        excluded_attrs (list): Contains attributes that were excluded by the user
        filtered_fields (list): Contains study fields which should the attributes come from

    Returns:
        list: Attibutes that should be displayed in the next form
    """
    # fields_with_approved_attrs = Characteristics.objects.filter(attribute__in=approved_attrs, field_of_study__in=filtered_fields).values_list('field_of_study',flat=True)
    # prefered_attrs = list(Characteristics.objects.filter(field_of_study__in=fields_with_approved_attrs).exclude(attribute__in=excluded_attrs).exclude(attribute__in=approved_attrs).order_by('?').values_list('attribute__id',flat=True))
    # prefered_attrs = list(dict.fromkeys(prefered_attrs))
    # other_attrs = list(Characteristics.objects.exclude(attribute__in=prefered_attrs).exclude(attribute__in=approved_attrs).exclude(attribute__in=excluded_attrs).order_by('?').values_list('attribute__id',flat=True))
    # other_attrs = list(dict.fromkeys(other_attrs))
    fields_with_approved_attrs = Characteristics.objects.filter(attribute__in=approved_attrs, field_of_study__in=filtered_fields).values_list('field_of_study',flat=True)
    prefered_attrs = Characteristics.objects.filter(field_of_study__in=fields_with_approved_attrs).exclude(attribute__in=approved_attrs).exclude(attribute__in=excluded_attrs).values_list('attribute__id',flat=True)
    prefered_attrs_sorted = [str(key) for key, value in sorted(Counter(prefered_attrs).items(), key=lambda item: item[1], reverse=True)]
    other_attrs = list(Characteristics.objects.exclude(attribute__in=prefered_attrs).exclude(attribute__in=approved_attrs).exclude(attribute__in=excluded_attrs).order_by('?').values_list('attribute__id',flat=True))
    other_attrs = list(dict.fromkeys(other_attrs))
    attrs_to_display = []
    proportion = 0.8
    len_of_attrs = 10
    added_other = 0
    added_prefered = 0
    for i in range(len_of_attrs):
        if added_prefered < int(len_of_attrs*proportion):
            if len(prefered_attrs_sorted) > 0:
                attrs_to_display.append(prefered_attrs_sorted[0])
                prefered_attrs_sorted.pop(0)
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
            elif len(prefered_attrs_sorted) > 0:
                attrs_to_display.append(prefered_attrs_sorted[0])
                prefered_attrs_sorted.pop(0)
                added_prefered += 1
    #print(f'{attrs_to_display} will be displayed with {added_prefered} prefered attrs and {added_other} other attrs.')
    return attrs_to_display

def DiscoverView(request):
    """Page that asks user to choose some attributes from the ones displayed.
    Then it adds them to appropriate lists and repeats the process until the max amount or
    repetitions is achieved or there are no more attributes to display.


    Returns:
        DiscoverView_results: Page that displays results of the DSS
    """
    if request.session['criteria']['characteristics'] == 0:
        return HttpResponseRedirect(reverse('DiscoverView_results'))
    else:
        approved_attributes = request.POST.getlist('approved')
        excluded_attributes = request.POST.getlist('all')
        
        
        # If both POST attributes are empty it meas that session should be initialized
        if approved_attributes == [] and excluded_attributes == []:
            #print('Clearing data')
            request.session['approved_attributes'] = []
            request.session['excluded_attributes'] = []
            request.session.modified=True
        else:
            request.session['approved_attributes'].extend(approved_attributes)

            excluded_attributes = [x for x in excluded_attributes if x not in approved_attributes]
            request.session['excluded_attributes'].extend(excluded_attributes)

            request.session['discover_try_attributes'] -= 1
            request.session.modified=True
        
        request.session['discover_progress'] += 1

        approved_attributes = request.session['approved_attributes']
        excluded_attributes = request.session['excluded_attributes']
        filtered_fields = request.session['filtered_fields']
        attrs_to_display = get_attributes_to_display(
            approved_attributes, excluded_attributes, filtered_fields
            )
        if request.session['discover_try_attributes'] > 0 and len(attrs_to_display) != 0:
            context = {
                'attrs':Attributes.objects.filter(id__in=attrs_to_display).all(),
                'progress': int(request.session['discover_progress']/request.session['discover_max_pages']*100)
            }
            return render(request, 'supporting_system/discover_view.html', context)
        else:
            return HttpResponseRedirect(reverse('DiscoverView_results'))

def DiscoverResultsView(request):
    """Result view for a DSS. It calculates the individual fit score for each study field.
    The score is a percentage of points that given subject got out of all th
    at could be possible
    to achieve (all which were displayed).
    """
    
    results_of_fields = defaultdict(float)
    city_score = request.session['criteria']['city']
    uni_score = request.session['criteria']['uni']
    uni_rank_score = request.session['criteria']['uni_rank']
    characteristics_score = 2*request.session['criteria']['characteristics']
    living_expenses_score = request.session['criteria']['living_expenses']
    best_score = city_score + uni_score + uni_rank_score + characteristics_score + living_expenses_score
    if characteristics_score != 0:
        shown_characteristics = []
        shown_characteristics = list(request.session['approved_attributes'])
        shown_characteristics.extend(list(request.session['excluded_attributes']))
    # Calculating final score for each field
    for field in request.session['filtered_fields']:
        characteristics_result = 0
        cities_result = 0
        uni_result = 0
        uni_rank_result = 0
        living_expenses_result = 0
        if characteristics_score != 0:
            approved_characteristics_of_field = Characteristics.objects.filter(field_of_study=field, attribute__id__in=request.session['approved_attributes']).values_list('fit',flat=True)
            shown_characteristics_of_field = Characteristics.objects.filter(field_of_study=field, attribute__id__in=shown_characteristics).values_list('fit',flat=True)
            characteristics_result = round(sum(approved_characteristics_of_field)/sum(shown_characteristics_of_field),2)
        if city_score != 0:
            if str(Field_of_Study.objects.get(id=field).university.city) in request.session['cities']:
                cities_result = 1
        
        if uni_score != 0:
            if str(Field_of_Study.objects.get(id=field).university.id) in request.session['university']:
                uni_result = 1

        if uni_rank_score != 0:
            uni_rank_result = round(1/Field_of_Study.objects.get(id=field).university.rank_overall,2)
        
        if living_expenses_score != 0:
            uni = Field_of_Study.objects.get(id=field).university
            avg_room_price = RoomPrice.objects.get(city=uni).avg_room_price/RoomPrice.objects.order_by('avg_room_price').first().avg_room_price
            living_expenses_result = round(1/avg_room_price,2)

        result = (city_score*cities_result + uni_score*uni_result + uni_rank_score*uni_rank_result + characteristics_score*characteristics_result + living_expenses_score*living_expenses_result)/best_score*100
        results_of_fields[field] = {
            'result':round(result,2),
            'characteristics':characteristics_result,
            'city':cities_result,
            'uni':uni_result,
            'uni_rank':uni_rank_result,
            'living_expenses':living_expenses_result,
        }
        #print(f'{field} got {result} points, {city_score*cities_result} from city, {uni_score*uni_result} from uni, {uni_rank_score*uni_rank_result} from uni rank and {characteristics_score*characteristics_result} from characteristics')

    results_of_fields = dict(sorted(results_of_fields.items(), key=lambda item: item[1]['result'], reverse=True))
    results_top3 = []
    results_rest = []
    for key, value in results_of_fields.items():
        temp_data_to_display = {
            'field':Field_of_Study.objects.get(id=key),
            'result':value['result'],
        }
        if characteristics_score != 0:
            temp_data_to_display['characteristics'] = [
                Characteristics.objects.filter(field_of_study=key, attribute__id__in=request.session['approved_attributes']).count(),
                Characteristics.objects.filter(field_of_study=key, attribute__id__in=shown_characteristics).count(),
                Characteristics.objects.filter(field_of_study=key).count(),
                True if Characteristics.objects.filter(field_of_study=key, attribute__id__in=request.session['approved_attributes']).count()/Characteristics.objects.filter(field_of_study=key, attribute__id__in=shown_characteristics).count() > 0.5 else False
                ]
        else:
            temp_data_to_display['characteristics'] = None

        if city_score != 0:
            temp_data_to_display['city'] = [
                value['city'],
                Field_of_Study.objects.get(id=key).university.city
                ]
        else:
            temp_data_to_display['city'] = None

        if uni_score != 0:
            temp_data_to_display['uni'] = [
                value['uni'],
                Field_of_Study.objects.get(id=key).university.name
                ]
        else:
            temp_data_to_display['uni'] = None

        if uni_rank_score != 0:
            temp_data_to_display['uni_rank'] = [
                value['uni_rank'],
                Field_of_Study.objects.get(id=key).university.rank_overall
                ]
        else:
            temp_data_to_display['uni_rank'] = None
        
        if living_expenses_score != 0:
            temp_data_to_display['living_expenses'] = [
                value['living_expenses'],
                RoomPrice.objects.get(city=Field_of_Study.objects.get(id=key).university).avg_room_price
                ]
        else:
            temp_data_to_display['living_expenses'] = None

        if len(results_top3) < 3:
            results_top3.append(temp_data_to_display)
        elif len(results_rest) < 10:
            results_rest.append(temp_data_to_display)
        else:
            break
        
    context = {
            'results_top3':results_top3,
            'results_rest':results_rest,
        }
    return render(request, 'supporting_system/discover_results_view.html', context)
