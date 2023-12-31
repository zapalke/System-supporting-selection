from django import template
from ..models import (
    Field_of_Study,
    University,
    Exam_Subjects,
    Characteristics,
    Alternative_Exam_Subjects,
    RoomPrice,
)
from django.db.models import Avg

register = template.Library()


@register.filter(name="return_field_of_study")
def return_field_of_study(id):
    obj = Field_of_Study.objects.get(id=id)
    return f"{obj.name} na uczelni {obj.university.name}"


@register.filter(name="return_subject_of_given_field")
def return_subject_of_given_field(id):
    obj = Exam_Subjects.objects.get(id=id)
    return f"{obj.subject} dla kierunku {obj.field_of_study.name} ({obj.field_of_study.university.name})"


@register.filter(name="return_characteristics_of_given_field")
def return_characteristics_of_given_field(id):
    obj = (
        Characteristics.objects.filter(field_of_study=id)
        .all()
        .order_by("attribute__attribute")
    )
    to_display = []
    for attribiute in obj:
        to_display.append(f"{attribiute.attribute} - {attribiute.fit}")
    return to_display


@register.filter(name="return_subjects_with_alternatives_of_given_field")
def return_subject_with_alternatives_of_given_field(id):
    obj = Exam_Subjects.objects.filter(field_of_study=id).all().order_by("subject")
    to_display = []
    for attribiute in obj:
        try:
            alternative_obj = (
                Alternative_Exam_Subjects.objects.filter(main_subject=attribiute.id)
                .all()
                .order_by("subject__subject")
            )
            temp_string = f"{attribiute.subject.subject}"
            for alternative_subject in alternative_obj:
                temp_string += f" lub {alternative_subject.subject.subject}"
            to_display.append(temp_string)
        except Alternative_Exam_Subjects.DoesNotExist:
            to_display.append(attribiute.subject.subject)
    if to_display == []:
        to_display = None
    return to_display


@register.filter(name="return_city_of_given_field")
def return_city_of_given_field(id):
    queryset = Field_of_Study.objects.get(id=id)
    return queryset.university.city


@register.filter(name="return_type_of_given_uni")
def return_type_of_given_uni(id):
    queryset = Field_of_Study.objects.get(id=id)
    return queryset.university.type


@register.filter(name="return_ranking_overall_of_given_uni")
def return_ranking_overall_of_given_uni(id):
    queryset = Field_of_Study.objects.get(id=id)
    return queryset.university.rank_overall


@register.filter(name="return_ranking_in_type_of_given_uni")
def return_ranking_in_type_of_given_uni(id):
    queryset = Field_of_Study.objects.get(id=id)
    return queryset.university.rank_in_type


@register.filter(name="return_current_filters")
def return_current_filters(initials: dict):
    next_url = f""
    for key, values in initials.items():
        if values != []:
            for val in values:
                next_url += f"&{key}={val}"
    return next_url


@register.filter(name="check_if_discover_url")
def check_if_discover_url(url):
    if "Discover" in url:
        return True
    else:
        return False


@register.filter(name="return_number_of_fields")
def return_number_of_field(degree):
    if degree != "Magister":
        return Field_of_Study.objects.exclude(degree="Magister").count()
    else:
        return Field_of_Study.objects.filter(degree="Magister").count()


@register.simple_tag(name="return_number_of_uni")
def return_number_of_uni():
    return University.objects.count()


@register.filter(name="living_expenses_below_avg")
def living_expenses_below_avg(living_expenses):
    avg_living_expenses = int(
        RoomPrice.objects.all().aggregate(Avg("avg_room_price"))["avg_room_price__avg"]
    )
    if living_expenses <= avg_living_expenses:
        return True
    else:
        return False
