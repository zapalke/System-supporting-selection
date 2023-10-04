from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (ListView, TemplateView, FormView)
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import AddUniversityForm
from .models import (Field_of_Study, University, Subjects,Exam_Subjects, 
                     Alternative_Exam_Subjects, Attribiutes, Characteristics)


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
            return render(request,'supporting_system/add_university_error.html',context)
        
        else:
            University.objects.create(**uni_data)

            if 'another' in request.POST:
                return HttpResponseRedirect(reverse('AddUniversityView'))
            else:
                return HttpResponseRedirect(reverse('ListUniversityView'))

class AddFieldView(LoginRequiredMixin, FormView):
    pass