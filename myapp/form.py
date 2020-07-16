from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Teacher, Pdf_file
from django.forms import ModelForm
from django.forms.widgets import DateTimeInput
# from datetimepicker.widgets import DateTimePicker







class signupform(UserCreationForm):
    matric_no = forms.IntegerField()
    course_of_study = forms.CharField(max_length=100)

    class Meta:
      model = User
      fields = ('first_name', 'last_name', 'username', 'email' )  
    

class studentloginform(forms.Form):
  username = forms.CharField(max_length=15)
  password = forms.CharField(widget=forms.PasswordInput)

class teacherloginform(ModelForm):
  
  class Meta:
    model = Teacher
    fields = ['last_name', 'code']  

class submitform(ModelForm):
  class Meta:
    model = Pdf_file
    fields = ['lecturer', 'document']


class gradeform(ModelForm):
  class Meta:
    model = Pdf_file
    fields = ['gradd']

class gradepoints(forms.Form):
  over_all_point = forms.IntegerField(min_value=1, max_value=99999)
  point = forms.IntegerField( min_value=1, max_value=99999) 
  

class setDateTime(forms.Form):

  to_datetime = forms.DateTimeField()  
 
 