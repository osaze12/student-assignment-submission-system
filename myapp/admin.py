# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Pdf_file) 
# admin.site.register(Submission_datetime)

