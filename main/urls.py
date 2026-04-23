from django import views
from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static

app_name = "main"
urlpatterns = [
    path('',views.HomePage,name='homepage'),
    path('thanhvien/login/', views.login_view, name='login'),
    path('thanhvien/logout/', views.logout_view, name='logout'),
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
    path('lasxd799/phep-thu/',views.PhepThuList,name='phepthu'),
    # Tin tức
    path('thong-bao/',views.NewsList,name='news'),
    path('quan-ly-tin-tuc/', views.news_manage, name='news_manage'),
    path('tin-tuc/them/', views.news_edit, name='news_add'),
    path('tin-tuc/sua/<int:pk>/', views.news_edit, name='news_edit'),
    path('tin-tuc/xoa/<int:pk>/', views.news_delete, name='news_delete'),
    path('thong-bao/<slug:slug>',views.NewsDetail,name='newsdetail'),
    # Liên hệ
    path('lien-he/',views.Contact,name='contact'),
    path('lien-he/quanly/', views.contact_manage, name='contact_manage'),
    path('lien-he/xoa/<int:pk>/', views.contact_delete, name='contact_delete'),
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

