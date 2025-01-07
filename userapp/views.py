from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from userapp.models import *
import urllib.request
import pandas as pd
import time
from adminapp.models import *
import urllib.parse
import random
import ssl


# Create your views here.






# ------------------------------------------------------------------------------------------------



#userviews



import pytz
from datetime import datetime



def user_dashboard(req):
    prediction_count = UserModel.objects.all().count()
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id=user_id)
    Feedbacks_users_count = Feedback.objects.all().count()
    all_users_count = UserModel.objects.all().count()

    if user.Last_Login_Time is None:
        IST = pytz.timezone("Asia/Kolkata")
        current_time_ist = datetime.now(IST).time()
        user.Last_Login_Time = current_time_ist
        user.save()
        return redirect("user_dashboard")

    return render(
        req,"user/User-Dashboard.html",
        {
            "predictions": prediction_count,
            "user_name": user.user_name,  
            "feedback_count": Feedbacks_users_count,
            "all_users_count": all_users_count,
        },
    )






def user_profile(req):
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id=user_id)
    if req.method == "POST":
        user_name = req.POST.get("username")
        user_age = req.POST.get("age")
        user_phone = req.POST.get("mobile_number")
        user_email = req.POST.get("email")
        user_password = req.POST.get("Password")
        user_address = req.POST.get("address")

        user.user_name = user_name
        user.user_age = user_age
        user.user_address = user_address
        user.user_contact = user_phone
        user.user_email = user_email
        user.user_password = user_password

        if len(req.FILES) != 0:
            image = req.FILES["profilepic"]
            user.user_image = image
            user.save()
            messages.success(req, "Updated Successfully.")
        else:
            user.save()
            messages.success(req, "Updated Successfully.")

    context = {"i": user}
    return render(req, "user/User-Profile2.html", context)


# ---------------------------------------------------------------------------------------------------------------


import os
from django.core.files.storage import default_storage
from django.contrib import messages
from django.conf import settings
from django.contrib import messages



from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

import os
import cv2
import numpy as np
from django.conf import settings

# Function to extract 50 frames for classification
def extract_frames_for_classification(video_path, max_frames=50):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames - 1, max_frames, dtype=int)  # Evenly spaced frame indices
    frames = []
    
    for frame_idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # Move to the selected frame
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))  # Resize to 224x224 for model input
        frames.append(frame)

    cap.release()

    # If fewer than max_frames, pad with black frames
    while len(frames) < max_frames:
        frames.append(np.zeros((224, 224, 3), dtype=np.uint8))

    return np.array(frames[:max_frames])  # Ensure exactly 50 frames

from django.core.files.storage import default_storage

# Function to extract 3 frames and save them as images for display
def extract_images_for_display(video_path, num_images=3):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames - 1, num_images, dtype=int)  # Evenly spaced frame indices
    saved_images = []  # To store the saved image URLs

    for count, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # Move to the selected frame
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))  # Resize to 224x224
        image_name = f"frame_{count}.jpg"
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        cv2.imwrite(image_path, frame)  # Save the frame as an image
        saved_images.append(default_storage.url(image_name))  # Save the URL to display later

    cap.release()
    
    return saved_images  # Return the saved image URLs

# Function to make a prediction using the model
def make_prediction(frames, model):
    frames = np.expand_dims(frames, axis=0)  # Add batch dimension (None, 50, 224, 224, 3)
    prediction = model.predict(frames)  # Make the prediction
    
    # Decode the prediction (assuming these are the 3 categories)
    categories = ['Explosion', 'Fighting', 'Shooting']
    predicted_class = categories[np.argmax(prediction, axis=1)[0]]
    
    return predicted_class  # Return the predicted class

# Load the trained model

# View to handle file upload and prediction





from django.shortcuts import render, redirect
from django.contrib import messages
import pickle

from django.shortcuts import render, redirect
from django.contrib import messages
import pickle
import sklearn

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
from tensorflow.keras.models import load_model

# Load the model (make sure this is in your views file)

def Classification(request):
    result = {"message": "No video uploaded"}  # Default result message
    uploaded_video_url = None

    if request.method == "POST" and 'video' in request.FILES:
        uploaded_video = request.FILES['video']
        
        # Save the video
        file_path = default_storage.save(uploaded_video.name, uploaded_video)
        path = settings.MEDIA_ROOT + '/' + file_path
        uploaded_video_url = default_storage.url(file_path)

        # Step 1: Extract frames for classification (50 frames)
        frames_for_classification = extract_frames_for_classification(path)
        
        # Step 2: Make prediction based on the extracted frames
        predicted_class = make_prediction(frames_for_classification, model)

        # Step 3: Extract 3 frames for display and save them as images
        saved_images = extract_images_for_display(path)
        
        # Store the result, video URL, and saved images in the session
        request.session['result'] = {"predicted_class": predicted_class}
        request.session['uploaded_video_url'] = uploaded_video_url
        request.session['saved_images'] = saved_images  # Store the image URLs

        # Add a success message with a prediction confidence level
        messages.success(request, f'Predicted class: {predicted_class} with confidence.')

        return redirect('Classification_result')  # Redirect to the result view
    
    return render(request, 'user/Prediction.html', {'result': result, 'uploaded_video_url': uploaded_video_url})


def Classification_result(request):
    result = request.session.get('result', {"message": "No result available"})
    uploaded_video_url = request.session.get('uploaded_video_url', None)
    saved_images = request.session.get('saved_images', [])  # Get saved image URLs

    return render(request, 'user/Prediction-result.html', {
        'result': result, 
        'uploaded_video_url': uploaded_video_url,
        'saved_images': saved_images  # Pass images to template
    })







# ------------------------------------------------------------------------------


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Feedback, UserModel  # Make sure to import your models


def user_feedback(req):
    id = req.session["user_id"]
    user = UserModel.objects.get(user_id=id)
    
    if req.method == "POST":
        rating = req.POST.get("rating")
        review = req.POST.get("review")
        
        # Sentiment analysis
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(review)
        
        if score["compound"] > 0 and score["compound"] <= 0.5:
            sentiment = "positive"
        elif score["compound"] >= 0.5:
            sentiment = "very positive"
        elif score["compound"] < -0.5:
            sentiment = "negative"
        elif score["compound"] < 0 and score["compound"] >= -0.5:
            sentiment = "very negative"
        else:
            sentiment = "neutral"
        
        # Create the feedback
        Feedback.objects.create(
            Rating=rating,
            Review=review,
            Sentiment=sentiment,
            Reviewer=user
        )
        
        messages.success(req, "Feedback recorded")
        return redirect("user_feedback")  # Redirecting to the same page
    
    return render(req, "user/User-Feedback.html")



from django.utils import timezone


def user_logout(req):
    if "user_id" in req.session:
        view_id = req.session["user_id"]
        try:
            user = UserModel.objects.get(user_id=view_id)
            user.Last_Login_Time = timezone.now().time()
            user.Last_Login_Date = timezone.now().date()
            user.save()
            messages.info(req, "You are logged out.")
        except UserModel.DoesNotExist:
            pass
    req.session.flush()
    return redirect("user_login")



def user_login(req):
    if req.method == "POST":
        user_email = req.POST.get("email")
        user_password = req.POST.get("password")
        print(user_email, user_password)

        try:
            users_data = UserModel.objects.filter(user_email=user_email)
            if not users_data.exists():
                messages.error(req, "User does not exist")
                return redirect("user_login")

            for user_data in users_data:
                if user_data.user_password == user_password:
                    if (
                        user_data.Otp_Status == "verified"
                    ):
                        req.session["user_id"] = user_data.user_id
                        messages.success(req, "You are logged in..")
                        user_data.No_Of_Times_Login += 1
                        user_data.save()
                        return redirect("user_dashboard")
                    elif (
                        user_data.Otp_Status == "verified"
                    ):
                        messages.info(req, "Your Status is in pending")
                        return redirect("user_login")
                    else:
                        messages.warning(req, "verifyOTP...!")
                        req.session["user_email"] = user_data.user_email
                        return redirect("otp")
                else:
                    messages.error(req, "Incorrect credentials...!")
                    return redirect("user_login")

            # Handle the case where no user data matched the password
            messages.error(req, "Incorrect credentials...!")
            return redirect("user_login")
        except Exception as e:
            print(e)
            messages.error(req, "An error occurred. Please try again later.")
            return redirect("user_login")

    return render(req, "user/user-login.html")

import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages



from django.contrib import messages



