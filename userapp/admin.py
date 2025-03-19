from django.contrib import admin

# Register your models here.
from . models import UserModel, PredictionResult


admin.site.register(UserModel)
admin.site.register(PredictionResult)
