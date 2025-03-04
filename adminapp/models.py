from django.db import models

# Create your models here.



class Upload_dataset_model(models.Model):
    user_id = models.AutoField(primary_key = True)
    Dataset = models.FileField(null=True)
    File_size = models.CharField(max_length = 100) 
    Date_Time = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'upload_dataset'

# dataset
class DATASET(models.Model):
    DS_ID = models.AutoField(primary_key = True)
    Age = models.IntegerField()
    PHYSICAL_SCORE = models.FloatField() 
    TEST_RESULTS = models.IntegerField()
    Pregnancies = models.IntegerField()
    
    class Meta:
        db_table = 'Dataset'




class ADA_ALGO(models.Model):
    S_NO = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'ADA_algo'

class RANDOM_ALGO(models.Model):
    S_NO = models.AutoField(primary_key = True)
    Accuracy = models.TextField(max_length = 100)
    Precession = models.TextField(max_length = 100) 
    F1_Score = models.TextField(max_length = 100)
    Recall = models.TextField(max_length = 100)
    Name = models.TextField(max_length = 100)
    
    class Meta:
        db_table = 'RANDOM_ALGO'


from django.db import models

class GRADIENT_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'GRADIENT_ALGO'

from django.db import models

class XG_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'XG_ALGO'

from django.db import models

from django.db import models

class RANDOM_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'RANDOM_ALGO'

class DECISION_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'DECISION_ALGO'

class LOGISTIC_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'LOGISTIC_ALGO'

class KNN_ALGO(models.Model):
    S_NO = models.AutoField(primary_key=True)
    Accuracy = models.TextField(max_length=100)
    Precession = models.TextField(max_length=100)
    F1_Score = models.TextField(max_length=100)
    Recall = models.TextField(max_length=100)
    Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'KNN_ALGO'



