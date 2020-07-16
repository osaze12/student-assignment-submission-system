
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from .form import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .form import *
from django.core.exceptions import ObjectDoesNotExist
from myapp.models import *

from django.contrib import messages

from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import calendar
from reportlab.pdfgen import canvas

# from.django.core.files import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

CURRENT_DATETIME = datetime.now()



# Create your views here.

def studentlogin(request):
  if request.method == 'POST':
      form = AuthenticationForm(request, request.POST)
      if form.is_valid():
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(username=username, password=password)
          if user is not None:
                login(request, user)
                return redirect('studentDashboard')
          else:
               messages.info(request, "Something went wrong")
               return redirect('studentlogin')
      else:
          messages.info(request, 'Sorry your name/password doesn\'t match')
          return redirect('studentlogin')
  else:
      form = studentloginform()  
  return render(request, 'myapp/studentlogin.html', {'form': form })

def sprofile(request):
    if request.user.is_authenticated and request.user.username !='admin':
        successful = Student.objects.get(user=request.user)
        if successful:
            return render(request, 'myapp/studentDashboard/profile.html', {'student': successful})
    else:
        messages.info(request, 'Please login first')
        return redirect('studentlogin')

def lprofile(request):
    if 'lecturer' in request.session:
        successful = Teacher.objects.get(last_name=request.session['lecturer'])
        if successful:
            return render(request, 'myapp/lecturerDashboard/profile.html', {'lecturer': successful})
    else:
        messages.info(request, 'Please login first')
        return redirect('teacherlogin')



# students able to view teachers that graded their assignment
def grade_result(request): 
    if request.user.is_authenticated:
       user = Student.objects.get(user=request.user)
       get_grade = Pdf_file.objects.filter(student=user, graded=True)
       return render(request, 'myapp/studentDashboard/results.html', {'grades': get_grade})
    else:
        messages.info(request, 'you are not logged in, please do, first.')
        return redirect('studentlogin')  

def teacherlogin(request):
    if request.method == 'POST':
        form = teacherloginform(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            last_name = f['last_name']
            code = f['code']
            try:
                e = Teacher.objects.get(code=code)
                if e.last_name == last_name:
                    request.session['lecturer'] = e.last_name
                    messages.info(request, 'Lecturer %s, You have successfully\
                    logged-in.' %request.session['lecturer'])

                    return redirect('lecturerDashboard')
                else:
                    messages.info(request, 'Sorry your name/code doesn\'t match')     
            except ObjectDoesNotExist:
                  messages.info(request, 'Lecturer Doesn\'t exist.')
                  return redirect('teacherlogin')
    else:
        form = teacherloginform()
    return render(request, 'myapp/teacherlogin.html', {'form': form })

def signup(request):
    if request.method == 'POST':
         form = signupform(request.POST)
        
         if form.is_valid():
            f = form.cleaned_data.get('matric_no')
            ff = Student.objects.filter(matric_no=str(f)).exists()
            if ff == False:
                user = form.save()
                user.refresh_from_db()
                user.student.matric_no = f
                user.student.course_of_study = form.cleaned_data.get('course_of_study')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                messages.info(request, 'you have Successfully Signup')
                return redirect('/studentDashboard')
            else:
                messages.info(request, 'Matric Number already exist, contact your Admin.')
    else:
        form = signupform()
    return render(request, 'myapp/signup.html', {'form':form})

def logoutall(request):
    logout(request)
    return redirect( 'studentlogin')


def lecturerlogout(request):
   
       if 'lecturer'in request.session:
         del request.session['lecturer']
         messages.info(request, 'You have successfully logged-out')
         return render(request, 'myapp/index.html')

       else: 
          return redirect( 'teacherlogin')
          
@login_required(login_url= '/studentlogin')
def submit_ass(request):
  if request.user.username !='admin':
     if request.method == 'POST':
        form = submitform(request.POST, request.FILES)

        if form.is_valid():
            get_pdf =str(request.FILES['document'])
            is_pdf = get_pdf[-4:]
            if is_pdf == '.PDF' or is_pdf == '.pdf':
                f = form.cleaned_data
                u = Student.objects.get(user=request.user)
                if u is not None: 
                    teacher = f['lecturer']
                    tea = Teacher.objects.get(last_name=teacher)
                    document = request.FILES['document']
                    #  check if the student submitted before
                    exist = Pdf_file.objects.filter(student=u.id, lecturer=tea).exists()
                    if exist:
                        messages.info(request, 'You already submitted before')
                    else:
                        if tea.from_datetime == None and tea.to_datetime == None:
                            messages.info(request, "lecturer hasn't set date/time for submission yet")
                        else:
                          #for this to work we've to replace the current tzinfo value to None
                                ff = tea.from_datetime.replace(tzinfo=None)
                                tt = tea.to_datetime.replace(tzinfo=None)
                        
                                if CURRENT_DATETIME >= ff and CURRENT_DATETIME <= tt:
                                    p =Pdf_file()
                                    p.student=u
                                    p.lecturer=tea
                                    p.document=document
                                    p.save()
                                    messages.info(request, 'You have successfully submitted')
                                    return redirect('studentDashboard')

                                elif CURRENT_DATETIME < ff:
                                    day = ff.day
                                    weekday = calendar.day_name[ff.weekday()]
                                    month = calendar.month_name[ff.month]
                                    year = ff.year
                                    messages.info(request, 'You can only submit\
                                    from {}th {}, of {}, {}'.format(day,weekday,month,year))

                                elif CURRENT_DATETIME > tt:
                                    day = tt.day
                                    weekday = calendar.day_name[tt.weekday()]
                                    month = calendar.month_name[tt.month]
                                    year = tt.year
                                    messages.info(request, 'Your date & time of submission has\
                                    passed {}th {}, of {}, {}'.format(day,weekday,month,year))
                else:
                  messages.info(request, 'Youre not logged in')
                  return redirect('studentlogin')
            else:
                messages.info(request, 'Invilid File format, only Pdf allowed')
     else:
        form = submitform()

     return render(request, 'myapp/studentDashboard/submit.html', {'form':form})
  else:
      messages.info(request, 'You are not allowed, youre an admin')
      return redirect('studentlogin')
  
def home(request):
    return render(request, 'myapp/index.html')
 
def studentDashboard(request):
    # An admin cannot login as student to submit assignments
    if request.user.is_authenticated and request.user.username !='admin' :
       student = Student.objects.get(user=request.user)
       return render(request, 'myapp/studentDashboard/studentDashboard.html', {'student':student})
    else:
        messages.info(request, 'You are not logged-in , please login first.')
        return redirect('studentlogin')

def lecturerDashboard(request):
    if 'lecturer'in request.session:
         lecturer_session_name = request.session['lecturer']
         lecturer_instance = Teacher.objects.get(last_name=lecturer_session_name)
         all_student_teacher_file_data = Pdf_file.objects.filter(lecturer=lecturer_instance)
        
         placeholder = {'to_datetime': 'Month/Day/Year H:M'}
         
         if request.method == 'POST':
             form = setDateTime(request.POST)
             get_form = form
             if get_form.is_valid():
                 #clean it, to have the value of the datetime 
                 f = get_form.cleaned_data
                 string_datetime = str(f['to_datetime'])
                 
                 from_datetime = CURRENT_DATETIME
                # convert string, to dateime object, to work
                 to_datetime= parse_datetime(string_datetime)
                 
        
                #  get model object
                 get_object = Teacher.objects.get(pk=lecturer_instance.id)
                 get_object.from_datetime = from_datetime
                 get_object.to_datetime = to_datetime

                 #delete other datetime object, before saving a new one
                 update = Teacher.objects.filter(pk=lecturer_instance.id).update(
                     from_datetime=None,to_datetime=None)

                 get_object.save()
                 messages.success(request, 'saved Successfully.')
                 return redirect('lecturerDashboard')
                 
              
         else:
             form = setDateTime(initial=placeholder)

         if lecturer_instance.from_datetime != None and lecturer_instance.to_datetime != None:
            g1= lecturer_instance.from_datetime
            xWeekDay1 = calendar.day_name[g1.weekday()]
            xMonth1 = calendar.month_name[g1.month]
            hold1 = {'day': g1.day, 'week': xWeekDay1,
             'month': xMonth1, 'year': g1.year, 'hr':g1.hour, 'min': g1.minute}

        #  ---------------------------------------------------------------------------------
            g2= lecturer_instance.to_datetime
            xWeekDay2 = calendar.day_name[g2.weekday()]
            xMonth2 = calendar.month_name[g2.month]
            hold2 = {'day': g2.day, 'week': xWeekDay2,
             'month': xMonth2, 'year': g2.year, 'hr':g2.hour, 'min': g2.minute}
         
       
            show = { 
             'lecturer':lecturer_session_name, 
             'oo': all_student_teacher_file_data,
             'form': form,
             'datetime': CURRENT_DATETIME,
             'xfrom': hold1,
             'xto': hold2,
            } 
            return render(request, 'myapp/lecturerDashboard/lecturerDashboard.html', show) 

         else:

            show = { 
             'lecturer':lecturer_session_name, 
             'oo': all_student_teacher_file_data,
             'form': form,
             'datetime': CURRENT_DATETIME,
            } 
            return render(request, 'myapp/lecturerDashboard/lecturerDashboard.html', show)

    else:
           messages.info(request, 'You are not logged-in , please login first.')
           return redirect('teacherlogin')


def edit_grade(request, lecturer, student):
    if 'lecturer'in request.session:
           if request.method == "POST":
                 form = gradepoints(request.POST)
                 if form.is_valid():
                     get_form_data = form.cleaned_data
                     point = float(get_form_data['point'])
                     overallpoint = float(get_form_data['over_all_point'])
                     divide_both =  (point/overallpoint)
                     answer = divide_both*100
                     answer_to_int = int(answer)

                     get_pdf_object =Pdf_file.objects.get(lecturer=lecturer, student=student)
                     get_pdf_object.point = answer_to_int
                     get_pdf_object.graded = True

                     

                     if answer_to_int in range(39):
                         get_pdf_object.gradd = 'F'
                     elif answer_to_int in range(39, 59):
                         get_pdf_object.gradd = 'E'
                     elif answer_to_int in range(59, 69):
                         get_pdf_object.gradd = 'D'
                     elif answer_to_int in range(69, 79):
                         get_pdf_object.gradd = 'C'
                     elif answer_to_int in range(79, 89):
                         get_pdf_object.gradd = 'B'
                     elif answer_to_int in range(79, 89):
                         get_pdf_object.gradd = 'A'
                     elif point > overallpoint:
                         get_pdf_object.gradd = "Error: Point is greater than Overall Point"

                     get_pdf_object.save()
                     return redirect('lecturerDashboard')
           else: 
                  form = gradepoints()
           return render(request, 'myapp/lecturerdashboard/editGrade.html', {'form':form })


    else:
         messages.info(request, 'You are not logged in, please do')
         return redirect('teacherlogin')

def listGradedAss(request):
    if 'lecturer'in request.session:

           lecturer = Teacher.objects.get(last_name =request.session['lecturer'] )
           listGradedAssignments = Pdf_file.objects.filter(lecturer=lecturer, graded=True)
           return render(request, 'myapp/lecturerDashboard/listGradedAssignments.html', {'listGraded':listGradedAssignments })
    else:
         messages.info(request, 'You are not logged in, please do')
         return redirect('teacherlogin')


def listNotGradedAss(request):
    if 'lecturer'in request.session:
        
           lecturer = Teacher.objects.get(last_name =request.session['lecturer'] )
           listNotGradedAssignments = Pdf_file.objects.filter(lecturer=lecturer,graded=False)
           
           return render(request, 'myapp/lecturerDashboard/listNotGradedAssignments.html', {'listNotGraded':listNotGradedAssignments })
    else:
         messages.info(request, 'You are not logged in, please do')
         return redirect('teacherlogin')

def view_ass(request, student):
    if 'lecturer' in request.session:
        lecturer = Teacher.objects.get(last_name=request.session['lecturer'])
        try:
           doc = Pdf_file.objects.get(lecturer=lecturer, student= student)
           if doc:
            pdfFile =str(doc.document)
            with open('media/'+pdfFile, 'rb') as pdf:
                response= HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename= %s' %pdfFile
                return response

        except ObjectDoesNotExist:
            return redirect('teacherlogin')
        
    else:
        messages.info(request, 'Please login first')
        return redirect( 'teacherlogin')