from django.contrib import admin

# Register your models here.

from . models import *

admin.site.register(Upload_dataset_model)
admin.site.register(ADA_ALGO)
admin.site.register(RANDOM_ALGO)
admin.site.register(GRADIENT_ALGO)
admin.site.register(XG_ALGO)
admin.site.register(DECISION_ALGO)
admin.site.register(LOGISTIC_ALGO)