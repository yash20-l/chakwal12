from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('home', views.home, name = "home"),
    path('verify', views.verify, name="verify"),
    path('logout', views.logoutUser, name='logout'),
    path('homework', views.Homework, name='homework'),
    path('homework/upload', views.UploadHomework, name='uploadhomework'),
    path('homework/download', views.DowloadHomework, name='downloadhomework'),
    # path('homework/download/<slug:myslug>', views.handleView, name='handleview'),
    path('like', views.postLikes, name='likePost'),
    path('chat', views.Chat, name = 'chat'),
    path('notifications', views.Notification, name = 'notifications'),
    path('motivation', views.Motivations, name='motivation'),
    path('fetchlikes', views.fetchLikes, name='ajaxCall'),
    path('profile', views.profile, name='profile'),
    path('changeprofile', views.changeProfile, name='changeprofile'),
    path('questions', views.questions, name='questions'),
    path('report', views.report, name='report'),
    path('notes', views.notes, name='notes')
]