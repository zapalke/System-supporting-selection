from django.urls import path, include

from .views import AddUniversityView, MainPageView, AddFieldView, AddSubjectsToFieldView, AddAlternativeSubjectsToFieldView,AddCharacteristicsView

urlpatterns = [
    path('', MainPageView.as_view(), name='MainPageView'),
    path('AddUniversityView', AddUniversityView.as_view(), name='AddUniversityView'),
    path('AddFieldView', AddFieldView.as_view(), name='AddFieldView'),
    path('AddSubjectsToFieldView/<str:field_of_study_id>/', AddSubjectsToFieldView.as_view(), name='AddSubjectsToFieldView'),
    path('AddAlternativeSubjectsToFieldView/<str:main_subject_id>/', AddAlternativeSubjectsToFieldView.as_view(), name='AddAlternativeSubjectsToFieldView'),
    path('AddCharacteristicsView/<str:field_of_study_id>/', AddCharacteristicsView.as_view(), name='AddCharacteristicsView')
    #path('ListUniversityView', AddUniversityView.as_view(), name='AddUniversityView')
]