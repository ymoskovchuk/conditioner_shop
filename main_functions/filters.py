import django_filters
from .models import *
from .choices import *


class ProductFilter(django_filters.FilterSet):

    recommended_area = django_filters.ChoiceFilter(choices=AREA_CHOICES)
    conditioner_type = django_filters.ChoiceFilter(choices=CONDITIONER_TYPE_CHOICES)
    invertor = django_filters.ChoiceFilter(choices=INVERTOR_CHOICES)

    class Meta:
        model = Product
        fields = ['brand']