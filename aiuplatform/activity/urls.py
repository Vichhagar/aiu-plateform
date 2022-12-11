from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    home, 
    JoinActivity, 
    CreateActivity, 
    ProfileHost, 
    ProfileJoin, 
    Moreinfo, 
    updateActivity, 
    deleteActivity, 
    leaveActivity,
    loginPage,
    register,
    logoutUser,
    updateUser,
    deleteUser
)
app_name = "activity"

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', register, name='register'),

    path('updateUser/<id>', updateUser, name='updateuser'),
    path('deleteUser/<id>', deleteUser, name='deleteuser'),

    path('', home, name='home'),
    path('join/', JoinActivity, name='join'),
    path('create/', CreateActivity, name='create'),
    path('dashboard/', ProfileHost, name='profile-host'),
    path('dashboard1/', ProfileJoin, name='profile-join'),
    path('more-info/<id>', Moreinfo, name='more-info'),
    path('update/<id>', updateActivity, name='update'),
    path('delete/<id>', deleteActivity, name='delete'),
    path('deleteActivity', leaveActivity, name='leave'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)