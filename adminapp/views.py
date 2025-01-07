from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from userapp.models import *
from adminapp.models import *
import urllib.request
import urllib.parse
import pandas as pd
from django.core.paginator import Paginator
from userapp.models import UserModel
from adminapp.models import *



# Create your views here.
def admin_dashboard(req):
    all_users_count = UserModel.objects.all().count()
    pending_users_count = UserModel.objects.filter(User_Status="pending").count()
    rejected_users_count = UserModel.objects.filter(User_Status="removed").count()
    accepted_users_count = UserModel.objects.filter(User_Status="accepted").count()
    Feedbacks_users_count = Feedback.objects.all().count()
    prediction_count = UserModel.objects.all().count()
    return render(
        req,
        "admin/Admin-dashboard.html",
        {
            "a": all_users_count,
            "b": pending_users_count,
            "c": rejected_users_count,
            "d": accepted_users_count,
            "e": Feedbacks_users_count,
            "f": prediction_count,
        },
    )


def pending_users(req):
    pending = UserModel.objects.filter(User_Status="pending")
    paginator = Paginator(pending, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/Pending-Users.html", {"user": post})


def all_users(req):
    all_users = UserModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/All-Users.html", {"user": post})



def delete_user(request, user_id):
    try:
        user = UserModel.objects.get(user_id=user_id)
        user.delete()
        messages.warning(request, "User was deleted successfully!")
    except UserModel.DoesNotExist:
        messages.error(request, "User does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect("all_users")



# Acept users button
def accept_user(request, id):
    try:
        status_update = UserModel.objects.get(user_id=id)
        status_update.User_Status = "accepted"
        status_update.save()
        messages.success(request, "User was accepted successfully!")
    except UserModel.DoesNotExist:
        messages.error(request, "User does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    
    return redirect("pending_users")




# Remove user button
def reject_user(req, id):
    status_update2 = UserModel.objects.get(user_id=id)
    status_update2.User_Status = "removed"
    status_update2.save()
    messages.warning(req, "User was Rejected..!")
    return redirect("pending_users")

# Change status users button
def change_status(request, id):
    user_data = UserModel.objects.get(user_id=id)
    if user_data.User_Status == "removed":
        user_data.User_Status = "accepted"
        user_data.save()
    elif user_data.User_Status == "accepted":
        user_data.User_Status = "removed"
        user_data.save()
    elif user_data.User_Status == "pending":
        messages.info(request, "Accept the user first..!")
        return redirect ("all_users")
    messages.success(request, "User status was changed..!")
    return redirect("all_users")







def adminlogout(req):
    messages.info(req, "You are logged out.")
    return redirect("admin_login")





def Comparision(request):
    

    return render(request, 'admin/Comparision.html')


    


def admin_Feedback(request):
    feed = Feedback.objects.all()
    return render(request, "admin/admin-Feedback.html", {"back": feed})
    

def admin_Sentimet_analysis(request):
    fee = Feedback.objects.all()
    return render(request, "admin/Sentiment-analysis.html", {"cat": fee})
    

def admin_Sentimet_analysis_graph(request):
    positive = Feedback.objects.filter(Sentiment="positive").count()
    very_positive = Feedback.objects.filter(Sentiment="very positive").count()
    negative = Feedback.objects.filter(Sentiment="negative").count()
    very_negative = Feedback.objects.filter(Sentiment="very negative").count()
    neutral = Feedback.objects.filter(Sentiment="neutral").count()
    context = {
        "vp": very_positive,
        "p": positive,
        "neg": negative,
        "vn": very_negative,
        "ne": neutral,
    }
    return render(request, "admin/Sentiment-analysis-graph.html",context)


