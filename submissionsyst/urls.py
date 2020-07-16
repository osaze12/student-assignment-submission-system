"""submissionsyst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views  
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^studentlogin/', views.studentlogin, name='studentlogin'),
    url(r'^slogout/', views.logoutall, name='logout'),
    url(r'^submit/', views.submit_ass, name='submit_ass'),
    url(r'^results/', views.grade_result, name='grade_result'),
    url(r'^studentDashboard/', views.studentDashboard, name='studentDashboard'),
    url(r'^studentprofile/', views.sprofile, name='sprofile'),





    

    url(r'^teacherlogin/', views.teacherlogin, name='teacherlogin'),
    url(r'^lecturerprofile/', views.lprofile, name='lprofile'),

    url(r'^llogout', views.lecturerlogout, name='lecturerlogout'),
    url(r'^lecturerDashboard/', views.lecturerDashboard, name='lecturerDashboard'),
    url(r'^gradedAssignments/', views.listGradedAss, name='listGradedAss'),
    url(r'^notGradedAssignments/', views.listNotGradedAss, name='listNotGradedAss'),
    url(r'^view/(?P<student>[0-9]+)', views.view_ass, name='view_ass'),



    


    
     
    url(r'^signup/', views.signup, name='signup'),
    url(r'^$', views.home, name='home'), 

    url(r'^edit_grade/(?P<lecturer>[0-9]+)/(?P<student>[0-9]+)/change/$', views.edit_grade, name='edit_grade'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 