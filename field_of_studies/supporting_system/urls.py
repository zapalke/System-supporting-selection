from django.urls import path, include

from .views import AddUniversityView, MainPageView, AddFieldView

urlpatterns = [
    path('', MainPageView.as_view(), name='MainPageView'),
    path('AddUniversityView', AddUniversityView.as_view(), name='AddUniversityView'),
    path('AddFieldView', AddFieldView.as_view(), name='AddFieldView'),
    #path('ListUniversityView', AddUniversityView.as_view(), name='AddUniversityView')
]