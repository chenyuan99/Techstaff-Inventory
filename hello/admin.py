from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportModelAdmin
class JobUpdateInline(admin.StackedInline):
    model = JobUpdate
    extra = 1
    max_num = 48

class JobApplicationAdmin(admin.ModelAdmin):
    inlines = [JobUpdateInline]
    model = JobApplication

    list_filter = (
        'place',
        'job_type',
        'active'
    )
    list_display = ('company', 'place', 'job_type', 'created_on', 'updated_on')

# admin.site.register(JobApplication, JobApplicationAdmin)
@admin.register(Desktop, Laptop, Mobile)
class ViewAdmin(ImportExportModelAdmin):
	pass
