from django.contrib import admin
from .models import (Field_of_Study, University, Subjects, Exam_Subjects, Alternative_Exam_Subjects,
                    Attributes, Characteristics)


class Field_of_StudyAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Field_of_Study._meta.fields]

class UniversityAdmin(admin.ModelAdmin):
    list_display = [column.name for column in University._meta.fields]

class SubjectsAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Subjects._meta.fields]

class Exam_SubjectsAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Exam_Subjects._meta.fields]

class Alternative_Exam_SubjectsAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Alternative_Exam_Subjects._meta.fields]

class AttributesAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Attributes._meta.fields]

class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = [column.name for column in Characteristics._meta.fields]


admin.site.register(Field_of_Study, Field_of_StudyAdmin)
admin.site.register(University,UniversityAdmin)
admin.site.register(Subjects,SubjectsAdmin)
admin.site.register(Exam_Subjects,Exam_SubjectsAdmin)
admin.site.register(Alternative_Exam_Subjects,Alternative_Exam_SubjectsAdmin)
admin.site.register(Attributes,AttributesAdmin)
admin.site.register(Characteristics, CharacteristicsAdmin)