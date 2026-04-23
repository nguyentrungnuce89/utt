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
    path('gioithieu/nhansu/manage/',views.NhansuManage,name='nhansumanage'),
    path('gioithieu/nhansu/<slug:slug>',views.NhansuDetail,name='nhansudetail'),
    path('lasxd799/trangthietbi/<int:id>',views.ThietbiDetail,name='thietbidetail'),
    path('gioithieu/dangkykinhdoanh/',views.Dkkd,name='dkkd'),
    path('gioithieu/ccnlhdxd/',views.Hdxd,name='hdxd'),
    path('lasxd799/',views.Lasxd,name='lasxd'),
    path('lasxd799/trangthietbi/',views.Thietbi,name='thietbi'),
    path('lasxd799/trangthietbi/manage/',views.ThietbiManage,name='thietbimanage'),
    path('du-an/',views.ProjectList,name='project'),
    path('du-an/manage/',views.ProjectManage,name='projectmanage'),
    path('update-project-full/', views.update_project_full, name='update_project_full'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete_project'),
    # Quản lý phép thử
    path('lasxd799/phep-thu/manage',views.PhepThuManage,name='phepthumanage'),
    path('update-phepthu-full/', views.update_phepthu_full, name='update_phepthu_full'),
    path('delete-phepthu/<int:pk>/', views.delete_phepthu, name='delete_phepthu'),  
    path('update-phepthu-order/', views.update_phepthu_order, name='update_phepthu_order'),
    path('lasxd799/phep-thu/',views.PhepThu,name='phepthu'),
    path('thong-bao/',views.News,name='news'),
    path('thong-bao/<slug:slug>',views.NewsDetail,name='newsdetail'),
    path('lien-he/',views.Contact,name='contact'),
    path('contact/submit/',views.Contact_submit),
    path('nhansu/reorder/',views.Reorder_nhansu,name='reorder_nhansu'),
    # API lấy dữ liệu Bằng cấp/Hợp đồng theo ID nhân sự
    path('get-hr-files/<int:pk>/', views.get_hr_files, name='get_hr_files'),
    # API lưu tổng thể hồ sơ
    path('update-hr-full/', views.update_hr_full, name='update_hr_full'),
    # DELETE profile photo
    path('delete-hr-photo/<int:pk>/', views.delete_hr_photo, name='delete_hr_photo'),
    # DELETE profile
    path('delete-personnel/<int:pk>/', views.delete_personnel, name='delete_personnel'),
    # Quản lý thiết bị
    path('update-thietbi-full/', views.update_thietbi_full, name='update_thietbi_full'),
    path('delete-thietbi/<int:pk>/', views.delete_thietbi, name='delete_thietbi'),
    path('get-hieuchuan-files/<int:pk>/', views.get_hieuchuan_files, name='get_hieuchuan_files'),
]

