from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^dashboard$',views.dashboard),
    url(r'^addpage',views.addpage),
    url(r'^add$',views.add),
    url(r'^edit/(?P<number>\d+)$',views.edit),
    url(r'^edit_page/(?P<id>\d+)$',views.edit_page),
    url(r'^logout$',views.logout),
    url(r'^delete/(?P<number>\d+)$',views.destroy),
    url(r'^go_back$', views.dashboard)
]