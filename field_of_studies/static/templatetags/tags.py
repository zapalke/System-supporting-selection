from django import template
from supporting_system.models import Field_of_Study,University, Exam_Subjects, Characteristics, Alternative_Exam_Subjects

register = template.Library()
@register.filter(name='check_if_discover_url')
def check_if_discover_url(url):
    if url.starswith('Discover'):
        return True
    else:
        return False