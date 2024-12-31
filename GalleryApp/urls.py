from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

from. views import Update
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',views.Gallery,name="gallery"),
    path('photo/<str:pk>/',views.View,name="photo"),
    path('add/',views.Add,name="add"),
    path('update/<str:pk>/',Update.as_view(),name="update"),
    path('delete/<str:pk>/',views.Delete.as_view(),name="delete"),
    path("login/",views.login_view,name="login"),
    path("register/",views.register,name="register"),
    path("logout/",LogoutView.as_view(next_page="login"),name="logout"),
    path("contact/",views.Contact,name="contact"),
    path("views/",views.views,name="views"),

    
]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)