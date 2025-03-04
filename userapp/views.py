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



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import PredictionResult

def user_dashboard(req):
    # Fetch predictions, feedback count, and user data
    prediction_count = PredictionResult.objects.all().count()
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id=user_id)
    Feedbacks_users_count = Feedback.objects.all().count()
    all_users_count = UserModel.objects.all().count()
    count = 0
    # Fetch all prediction results
    prediction_results = PredictionResult.objects.filter(email=user.user_email).order_by('-timestamp')
    return render(
        req, "user/User-Dashboard.html",
        {
            "predictions": prediction_count,
            "user_name": user.user_name,
            "feedback_count": Feedbacks_users_count,
            "all_users_count": all_users_count,
            "prediction_results": prediction_results,
            'count':count,
        },
    )

# View to delete a prediction
def delete_prediction(request, prediction_id):
    # Get the prediction object by ID
    prediction = get_object_or_404(PredictionResult, id=prediction_id)

    # Delete the prediction object
    prediction.delete()

    # Redirect back to the dashboard or wherever necessary
    return redirect('user_dashboard')  # Redirect to the user dashboard or a success page







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


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from userapp.models import *
import urllib.request
import pandas as pd
import time

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from tensorflow.keras.applications.densenet import preprocess_input
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
import os
import random  # For generating a 4-digit pin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from mainapp.models import *
# Load the model and other necessary imports
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.applications.densenet import preprocess_input

# Assuming you already have a loaded model, e.g., `model`
model = load_model('Oil Spil Dataset/oil_densenet.h5')

def predictionss(image_path):
    """This function makes predictions on the image at the provided path."""
    img = image.load_img(image_path, target_size=(224, 224))  # Load image and resize
    i = image.img_to_array(img)  # Convert image to array
    i = np.expand_dims(i, axis=0)  # Expand dimensions to match model input
    img = preprocess_input(i)  # Preprocess image (e.g., normalization)
    pred = np.argmax(model.predict(img), axis=1)  # Get the predicted class
    return pred[0]  # Return the predicted class index (ensure it’s an int)
import json  # Add this import
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import datetime
import os
from django.conf import settings
from .models import PredictionResult
import base64
import io
# Load the pre-trained model
model = load_model('Oil Spil Dataset/oil_densenet.h5')

def predictionss(image_data):
    """This function makes predictions on the image provided."""
    # Decode the image from base64
    img_data = base64.b64decode(image_data.split(',')[1])
    img = Image.open(io.BytesIO(img_data))

    # Resize the image
    img = img.resize((224, 224))
    
    # Convert to array and preprocess
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Normalize if required
    
    # Predict the class
    pred = np.argmax(model.predict(img_array), axis=1)
    return pred[0]

def live_camera_prediction(request):
    """Handle the live cam image predictions."""
    if request.method == "POST":
        # Receive the image data from the webcam
        data = json.loads(request.body)  # Ensure json is imported
        image_data = data.get('image')
        
        # Make prediction
        predicted_class = predictionss(image_data)

        # If oil spill detected, send email alert
        if predicted_class == 1:
            email = data.get('email')
            if email and '@' in email:
                mail_message = "Oil Spill Detected!"
                send_mail(
                    "Alert!",
                    mail_message,
                    settings.EMAIL_HOST_USER,
                    [email],
                )

        return JsonResponse({"prediction": predicted_class}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

import os
import datetime
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PredictionResult  # Assuming you created this model

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from django.conf import settings

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime
from django.conf import settings

def generate_pdf(predicted_class, email, uploaded_image_url):
    # Define the path where the PDF should be saved
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'prediction_pdfs')
    
    # Ensure the directory exists
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)  # Create the directory if it doesn't exist
    
    # Generate a unique filename for the PDF
    file_path = os.path.join(pdf_directory, f"prediction_result_{str(datetime.datetime.now().timestamp())}.pdf")
    
    # Create the PDF
    pdf = canvas.Canvas(file_path, pagesize=letter)
    pdf.setFont("Helvetica", 14)

    # Set up a margin for layout
    margin_left = 72
    margin_top = 750
    
    # Title/Header - Centered and Bold
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString((letter[0] - pdf.stringWidth("Prediction Result for Oil Spill Detection", "Helvetica-Bold", 16)) / 2, margin_top, "Prediction Result for Oil Spill Detection")
    
    # Move down and add Prediction
    margin_top -= 30
    prediction_text = "Prediction: " + ("Oil Spill" if predicted_class == 1 else "No Oil Spill")
    pdf.drawString((letter[0] - pdf.stringWidth(prediction_text, "Helvetica-Bold", 16)) / 2, margin_top, prediction_text)
    
    # Move down for email and date/time (Italicized)
    margin_top -= 40
    pdf.setFont("Helvetica-Oblique", 12)  # Italicize the text
    pdf.drawString(margin_left, margin_top, f"Email: {email}")
    margin_top -= 20
    pdf.drawString(margin_left, margin_top, f"Date & Time: {str(datetime.datetime.now())}")

    # Reset font for the remaining content
    pdf.setFont("Helvetica", 12)
    margin_top -= 40  # Move down for the next section
    
    # Image URL
    pdf.drawString(margin_left, margin_top, f"Image URL: {uploaded_image_url}")
    
    # Move down and start adding precautions content
    margin_top -= 60
    precautions = """
    Oil spills can cause significant harm to marine ecosystems. 
    If an oil spill is detected, immediate action should be taken:
    - Stop the source of the spill if safe to do so.
    - Contain the spill using barriers and absorbent materials.
    - Contact relevant authorities for further assistance.
    """
    
    # Add precaution text with line wrapping
    text_object = pdf.beginText(margin_left, margin_top)
    text_object.setFont("Helvetica", 12)
    text_object.setTextOrigin(margin_left, margin_top)
    text_object.setLeading(14)  # Space between lines
    text_object.textLines(precautions)  # Automatically wraps the text
    
    # Draw the precaution text block
    pdf.drawText(text_object)
    
    # Add footer with city and current details
    margin_top -= 120  # Move down for footer
    pdf.setFont("Helvetica", 10)
    pdf.drawString(margin_left, margin_top, f"City: Nambur")
    margin_top -= 20
    pdf.drawString(margin_left, margin_top, f"Date & Time of Detection: {str(datetime.datetime.now())}")

    # Save the PDF to the specified path
    pdf.save()

    # Return the relative file path for storing in the database
    return os.path.relpath(file_path, settings.MEDIA_ROOT)

import os
import cv2
import base64
import datetime
import numpy as np
import matplotlib.pyplot as plt
import io
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from .models import PredictionResult

# Load the model
model = load_model('Oil Spil Dataset/oil_densenet.h5')

def predictionss(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return np.argmax(prediction, axis=1)[0]

def generate_rgb_image(image_path):
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    color_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_JET)
    rgb_image_path = os.path.splitext(image_path)[0] + '_colorized.jpg'
    cv2.imwrite(rgb_image_path, color_image)
    return rgb_image_path

def generate_segmented_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    segmented_image_path = os.path.splitext(image_path)[0] + '_segmented.jpg'
    cv2.imwrite(segmented_image_path, binary_image)
    return segmented_image_path

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def Classification(request):
    if request.method == "POST" and 'image' in request.FILES:
        uploaded_image = request.FILES['image']
        file_path = default_storage.save(uploaded_image.name, uploaded_image)
        image_path = os.path.join(settings.MEDIA_ROOT, file_path)
        uploaded_image_url = default_storage.url(file_path)

        # Predict the class of the image
        predicted_class = predictionss(image_path)

        # Generate processed images
        rgb_image_path = generate_rgb_image(image_path)
        segmented_image_path = generate_segmented_image(image_path)

        # Convert images to base64 for display
        uploaded_image_base64 = encode_image(image_path)
        rgb_image_base64 = encode_image(rgb_image_path)
        segmented_image_base64 = encode_image(segmented_image_path)

        # Determine prediction result
        prediction_text = "Oil Spill Detected" if predicted_class == 1 else "No Oil Spill Detected"
        user_id = request.session.get("user_id")
        user = UserModel.objects.get(user_id=user_id)
        # Alert email if Oil Spill is detected
        if predicted_class == 1:
            user_id = request.session.get("user_id")
            if user_id:
                try:
                    user = UserModel.objects.get(user_id=user_id)
                    email = user.user_email  # Assuming your UserModel has an email field
                    
                    if email and '@' in email:
                        alert_message = "ALERT! Oil Spill has been detected in the uploaded image."
                        send_mail(
                            "Oil Spill Detection Alert",
                            alert_message,
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                        messages.warning(request, "An alert email has been sent to your registered email address.")
                    else:
                        messages.error(request, "No valid email address found in your profile.")
                except UserModel.DoesNotExist:
                    messages.error(request, "User not found. Please log in again.")
            else:
                messages.error(request, "You must be logged in to receive email alerts.")
        email = user.user_email
        print(email)
        pdf_file_path = generate_pdf(predicted_class, email, uploaded_image_url)
        print(pdf_file_path)
        # Save the prediction result in the database
        prediction_record = PredictionResult(
            predicted_class=predicted_class,
            email=user.user_email,
            pdf_file=pdf_file_path,
            image_url=uploaded_image_url,
            timestamp=datetime.datetime.now()
        )
        prediction_record.save()

        # Store results in session
        request.session['result'] = {"predicted_class": int(predicted_class)}
        request.session['uploaded_image_url'] = uploaded_image_url
        request.session['rgb_image_path'] = rgb_image_path
        request.session['segmented_image_path'] = segmented_image_path
        prediction = PredictionResult.objects.last()  # Or use the specific query to get this prediction

        
        pdf_url = None
        if prediction:
            pdf_url = default_storage.url(prediction.pdf_file)  # Get the URL for downloading the PDF
            print(pdf_url)

        
        messages.warning(request, f'Alert! Predicted class: {predicted_class}. {prediction_text}')
        result = request.session.get('result', {"message": "No result available"})
        prediction_text = "Oil Spill Detected" if result.get('predicted_class') == 1 else "No Oil Spill Detected"
        return render(request,'user/Prediction-result.html', {'result':result,'prediction': prediction_text,'uploaded_image_url':uploaded_image_url, 'rgb_image_base64':rgb_image_base64, 'segmented_image_base64' : segmented_image_base64, 'pdf_url': pdf_url,})
    
    return render(request, 'user/Prediction.html')

def Classification_result(request):
    result = request.session.get('result', {"message": "No result available"})
    uploaded_image_url = request.session.get('uploaded_image_url', None)
    rgb_image_path = request.session.get('rgb_image_path', None)
    segmented_image_path = request.session.get('segmented_image_path', None)

    # Encode images to base64
    uploaded_image_base64 = encode_image(os.path.join(settings.MEDIA_ROOT, uploaded_image_url.lstrip('/')))
    rgb_image_base64 = encode_image(rgb_image_path)
    segmented_image_base64 = encode_image(segmented_image_path)

    prediction_text = "Oil Spill Detected" if result.get('predicted_class') == 1 else "No Oil Spill Detected"

    return render(request, 'user/Prediction-result.html', {
        'result': result,
        'uploaded_image': uploaded_image_base64,
        'rgb_image': rgb_image_base64,
        'segmented_image': segmented_image_base64,
        'prediction': prediction_text,
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
    return redirect("index")



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
                        and user_data.User_Status == "accepted"
                    ):
                        req.session["user_id"] = user_data.user_id
                        messages.success(req, "You are logged in..")
                        user_data.No_Of_Times_Login += 1
                        user_data.save()
                        return redirect("user_dashboard")
                    elif (
                        user_data.Otp_Status == "verified"
                        and user_data.User_Status == "pending"
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



