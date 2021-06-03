import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):

    AREA_CHOICES = (
        ('20', '20'),
        ('25', '25'),
    )
    recommended_area = django_filters.ChoiceFilter(choices=AREA_CHOICES)

    class Meta:
        model = Product
        fields = ['brand', 'producer', ]