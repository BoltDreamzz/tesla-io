from django.urls import path
from . import views



urlpatterns = [
    path('', views.qfs_home, name='qfs_home'),
    path('med-beds/', views.med_beds, name='med_beds'),
    path('start_qfs/', views.start_qfs, name='start_qfs'),
    path("start/", views.qfs_start, name="qfs_start"),
    path("qfs/cards/", views.qfs_cards, name="qfs_cards"),
    path("qfs/details/", views.qfs_details, name="qfs_details"),
    path("qfs/success/", views.qfs_success, name="qfs_success"),

]