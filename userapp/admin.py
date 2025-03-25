from django.contrib import admin

# Register your models here.
# from . models import UserModel, PredictionResult


# admin.site.register(UserModel)
# admin.site.register(PredictionResult)
from . models import *


admin.site.register(UserModel)
admin.site.register(PredictionResult)
admin.site.register(Predict_details)
admin.site.register(PredictionCount)
admin.site.register(Last_login)
admin.site.register(Contact_Us)
admin.site.register(Feedback)