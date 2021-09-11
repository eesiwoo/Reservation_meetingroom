# from django.conf.urls import url
from django.urls import path
from reservation import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('rez_list/', views.ListView.as_view(), name='list'),
    path('hidden/', views.Hidden.as_view(), name='hidden'),
    path('rez_list/rezlist/', views.rezList, name='rezlist'),
    path('addRez/', views.AddRezView.as_view(), name='addrez'),
    path('addRez/timecheck/', views.timecheck, name='timecheck'),
    path('addRez/usercheck/', views.usercheck, name='usercheck'),
    path('addRez/search/', views.search, name='search'),
    path('addRez/rezlist/', views.rezList, name='rezlist'),
    path('newRez', views.NewRezView.as_view(), name='newrez'),
    path('add_outsider/', views.AddOutsiderView.as_view(), name='addoutsider'),
    path('add_outsider/do_duplicate_check/', views.do_duplicate_check, name='do_duplicate_check'),
    path('add_outsider/email_check/', views.email_check, name='email_check'),
    path('add_outsider/phone_check/', views.phone_check, name='phone_check'),
    path('modify_rez/', views.ModifyRezView.as_view(), name='modify'),
    path('my_future_rez/', views.FutureRezView.as_view(), name='future'),
    path('my_future_rez/<int:pk>/delete/', views.delete, name='delete'),
    path('my_past_rez/', views.PastRezView.as_view(), name='past'),
    path('outsider_list/', views.OutsiderListView.as_view(), name='outsiderlist'),
    path('outsider_list/bbs_search/', views.bbs_search, name='bbs_search'),
    path('tbl_base/', views.TblView.as_view(), name='tbl_base'),
    path('editRez', views.EditRezView.as_view(), name='editrez'),
    path('timecheck/', views.timecheck, name='timecheck'),
    path('usercheck/', views.usercheck, name='usercheck'),
    path('search/', views.search, name='search'),
    path('editRez/rezlist/', views.rezList, name='rezlist'),
    path('hidden/rezlist/', views.rezList, name='rezlist'),
    path('rezlist/', views.rezList, name='rezlist'),
]
