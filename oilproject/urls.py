"""
URL configuration for oilproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


"""
URL configuration for hearing_project project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from userapp import views as user_views
from adminapp import views as admin_views
from mainapp import views as mainapp_views

# URLS
urlpatterns = [
    # Main_Urls
    path('admin/', admin.site.urls),
    path('',mainapp_views.index,name='index'),
    path('about-us',mainapp_views.about_us,name='about_us'),
    path('user-login',mainapp_views.user_login,name='user_login'),
    path('admin-login',mainapp_views.admin_login,name='admin_login'),
    path('contact-us',mainapp_views.contact_us,name='contact_us'),
    path('register',mainapp_views.register,name='register'),
    path('otp',mainapp_views.otp,name='otp'),
    path('delete_prediction/<int:prediction_id>/', user_views.delete_prediction, name='delete_prediction'),
    path('predict-oil-spill/', user_views.live_camera_prediction, name='live_oil_spill_prediction'),

    #User Views
    path('user-dashboard',user_views.user_dashboard,name='user_dashboard'),
    path('user-profile',user_views.user_profile,name='user_profile'),
    path('prediction',user_views.Classification,name='Classification'),
    path('prediction-result',user_views.Classification_result,name='Classification_result'),
    path('user-feedback',user_views.user_feedback,name='user_feedback'),
    path('user-logout',user_views.user_logout,name='user_logout'),

    


    #URLS_admin
    
    path('admin-dashboard',admin_views.admin_dashboard,name='admin_dashboard'),
   

    path('pending-users',admin_views.pending_users,name='pending_users'),
    path('all-users', admin_views.all_users, name='all_users'),
    path('delete-user/<int:user_id>/', admin_views.delete_user, name='delete_user'),

    path('accept-user/<int:id>', admin_views.accept_user, name = 'accept_user'),
    path('reject-user/<int:id>', admin_views.reject_user, name = 'reject'),
    path('change-status/<int:id>', admin_views.change_status, name = 'change_status'),
    path('adminlogout',admin_views.adminlogout, name='adminlogout'),

    path('admin-feedback',admin_views.admin_Feedback,name='admin_feedback'),
    path('sentiment-analysis', admin_views.admin_Sentimet_analysis, name = 'sentiment_analysis'),
    path('sentiment-analysis-graph',admin_views.admin_Sentimet_analysis_graph,name='sentiment_analysis_graph'),

    path('Comparision', admin_views.Comparision, name = 'Comparision'),
    path('admin_Feedback', admin_views.admin_Feedback, name = 'admin_Feedback'),
    path('admin_Sentimet_analysis', admin_views.admin_Sentimet_analysis, name = 'admin_Sentimet_analysis'),
    path('admin_Sentimet_analysis_graph', admin_views.admin_Sentimet_analysis_graph, name = 'admin_Sentimet_analysis_graph'),


    
    
    # path('Extra_tree', admin_views.Extra_tree, name = 'Extra_tree'),
    # path('Extra_tree_btn/', admin_views.Extra_tree_btn, name = 'Extra_tree_btn'),
    # path('admin-feedback',admin_views.admin_feedback,name='admin_feedback'),
    # path('sentiment-analysis', admin_views.sentiment_analysis, name = 'sentiment_analysis'),
    # path('sentiment-analysis-graph',admin_views.sentiment_analysis_graph,name='sentiment_analysis_graph'),
    # path('comparision-graph',admin_views.comparision_graph,name='comparision_graph'),

]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



