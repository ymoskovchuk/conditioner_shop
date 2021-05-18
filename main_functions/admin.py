from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin

from .models import *


class ConditionerAdminForm(ModelForm):

    MIN_RESOLUTION = (700, 400)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Завантажуйте зображення з мінімальними розмірами {}x{}'.format(
            *self.MIN_RESOLUTION
        )


class ConditionerAdmin(admin.ModelAdmin):

    form = ConditionerAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='conditioners'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class InvertorAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='invertors'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Conditioner, ConditionerAdmin)
admin.site.register(Invertor, InvertorAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)