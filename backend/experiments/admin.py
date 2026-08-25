from django.contrib import admin
from .models import Experiment, ExposureBand, DayConversion, HourConversion


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['name', 'decision', 'statistically_significant', 'absolute_uplift', 'created_at']


admin.site.register(ExposureBand)
admin.site.register(DayConversion)
admin.site.register(HourConversion)
