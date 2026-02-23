from django.urls import path
from .views import *

app_name = "Student"

urlpatterns = [

    path('stdhome/', stdHome.as_view(), name='stdhome'),

    path('mycertificates/', MyIssuedCertificatesView.as_view(), name='my_certificates'),

    path('certificate/<int:pk>/', 
         CertificateDetailView.as_view(), 
         name='certificate_detail'),

    path('certificate/<int:pk>/download/', 
         CertificateDownloadView.as_view(), 
         name='download_certificate'),

    path('course-materials/', 
         StudentCourseMaterialsView.as_view(), 
         name='student_course_materials'),

    path('feedback/<int:certificate_id>/', 
         FeedbackCreateView.as_view(), 
         name='feedback_create'),
    
    path("courseratings/", CourseRatingsView.as_view(), name="course_ratings"),     
]
