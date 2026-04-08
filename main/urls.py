from django import views
from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static

app_name = "main"
urlpatterns = [
    path('',views.HomePage,name='homepage'),
    path('gioithieu/',views.About,name='about'),
    path('gioithieu/nhansu/',views.Nhansu,name='nhansu'),
    path('gioithieu/nhansu/<slug:slug>',views.NhansuDetail,name='nhansudetail'),
    path('gioithieu/dangkykinhdoanh/',views.Dkkd,name='dkkd'),
    path('gioithieu/ccnlhdxd/',views.Hdxd,name='hdxd'),
    path('gioithieu/lasxd799/',views.Lasxd,name='lasxd'),
    path('gioithieu/trangthietbi/',views.Thietbi,name='thietbi'),
    path('du-an/',views.Project,name='project'),
    path('phep-thu/',views.PhepThu,name='phepthu'),
    path('thong-bao/',views.News,name='news'),
    path('thong-bao/<slug:slug>',views.NewsDetail,name='newsdetail'),
    path('lien-he/',views.Contact,name='contact'),
    path('contact/submit/',views.Contact_submit)
]

