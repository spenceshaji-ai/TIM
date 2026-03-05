from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from tims.users.views import LoginView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("", TemplateView.as_view(template_name="pages/adminhome.html"), name="home"),
    path("about/",TemplateView.as_view(template_name="pages/about.html"),name="about",),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),

    # Auth
    path("accounts/", include("allauth.urls")),
    
    path("users/", include("tims.users.urls", namespace="users")),

    path("adminapp/", include("tims.adminapp.adminapp_urls")),

    path("facultyapp/",include("tims.facultyapp.faculty_url" )),

    path("Admin/",include("tims.Admin.admin_urls" )),
    
    path("Student/", include("tims.Student.studentapp_urls")),



    
    
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# ✅ Serve Media Files in Development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


[path("Student/", include("tims.Student.studentapp_urls", namespace="Student")),
]
# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Error pages
    urlpatterns += [
        path("400/",default_views.bad_request,kwargs={"exception": Exception("Bad Request!")},),
        path("403/",default_views.permission_denied,kwargs={"exception": Exception("Permission Denied")},),
        path("404/",default_views.page_not_found,kwargs={"exception": Exception("Page not Found")},),
        path("500/", default_views.server_error),
    ]

    # Debug toolbar
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            
        ] + urlpatterns

