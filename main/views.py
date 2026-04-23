from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:homepage') # Nếu đã login thì về trang chủ

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:homepage')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Thông tin đăng nhập không hợp lệ.")
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:homepage')

def HomePage(request):
    context = {}
    return render(request,'homepage.html',context)

def About(request):
    context = {}
    return render(request,'about.html',context)

# Trang danh sách quản lý liên hệ
@login_required
def contact_manage(request):
    from .models import Contact
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact_manage.html', {'contacts': contacts})

# API Xóa liên hệ
@login_required
def contact_delete(request, pk):
    from .models import Contact
    if request.method == 'POST':
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def Nhansu(request):
    from .models import HR
    nhansu = HR.objects.filter(Visibility=True).order_by('STT')
    context = {
        'nhansu':nhansu
    }
    return render(request,'a_nhansu.html',context)

@login_required
def NhansuManage(request):
    from .models import HR
    nhansu = HR.objects.all().order_by('STT')
    context = {
        'nhansu':nhansu
    }
    return render(request,'a_nhansu_manage.html',context)

def NhansuDetail(request,slug):
    from .models import HR,Degree,HopDong
    member = get_object_or_404(HR, slug=slug)
    degrees = Degree.objects.filter(Owner=member).order_by('-Date')
    contracts = HopDong.objects.filter(NguoiKy=member)
    context = {
        'i':member,
        'degrees': degrees,
        'contracts':contracts
    }
    return render(request,'nhansu_detail_new.html',context)

def Dkkd(request):
    context = {}
    return render(request,'a_dkkd.html',context)

def Hdxd(request):
    context = {}
    return render(request,'a_hdxd.html',context)

def Lasxd(request):
    from .models import ThanhLapPhong
    qds = ThanhLapPhong.objects.filter(Visibility=True)
    context = {
        'qds':qds
    }
    return render(request,'b_lasxd.html',context)

def QuyetDinh(request):
    from .models import ThanhLapPhong
    qds = ThanhLapPhong.objects.filter(Visibility=True)
    context = {
        'qds':qds
    }
    return render(request,'b_decisions.html',context)

from .models import ThanhLapPhong

# Trang danh sách quản lý
def quyetdinh_manage(request):
    items = ThanhLapPhong.objects.all().order_by('-Ngay')
    return render(request, 'b_decision_manage.html', {'items': items})

# API Thêm/Sửa Quyết định
def quyetdinh_update(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        ten = request.POST.get('Ten')
        ngay = request.POST.get('Ngay') or None
        visibility = True if request.POST.get('Visibility') == 'on' else False
        file_upload = request.FILES.get('File')

        try:
            if item_id: # SỬA
                item = get_object_or_404(ThanhLapPhong, id=item_id)
                item.Ten = ten
                item.Ngay = ngay
                item.Visibility = visibility
                if file_upload:
                    item.File = file_upload
                item.save()
            else: # THÊM MỚI
                ThanhLapPhong.objects.create(
                    Ten=ten, Ngay=ngay, File=file_upload, Visibility=visibility
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# API Xóa Quyết định
def quyetdinh_delete(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(ThanhLapPhong, pk=pk)
        item.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)



def Thietbi(request):
    from .models import ThietBi
    thietbis = ThietBi.objects.filter(Visibility=True).order_by('Nhom','STT')
    from collections import defaultdict
    nhomthietbi = defaultdict(list)
    for i in thietbis:
        nhomthietbi[i.Nhom].append(i)
    for nhom in nhomthietbi:
        nhomthietbi[nhom] = sorted(nhomthietbi[nhom], key=lambda x: x.STT)
    context = {
        'thietbi':dict(nhomthietbi)
    }
    return render(request,'b_thietbi.html',context)

def ThietbiDetail(request,id):
    from .models import ThietBi,HieuChuan
    ins = get_object_or_404(ThietBi,id=id)
    hieuchuan = HieuChuan.objects.filter(May=ins).order_by('-Ngay')
    context = {
        'i':ins,
        'hcs':hieuchuan
    }
    return render(request,'thietbi_detail.html',context)

@login_required
def ThietbiManage(request):
    from .models import ThietBi
    thietbis = ThietBi.objects.filter(Visibility=True).order_by('Nhom','STT')
    from collections import defaultdict
    nhomthietbi = defaultdict(list)
    for i in thietbis:
        nhomthietbi[i.Nhom].append(i)
    for nhom in nhomthietbi:
        nhomthietbi[nhom] = sorted(nhomthietbi[nhom], key=lambda x: x.STT)
    context = {
        'thietbi':dict(nhomthietbi)
    }
    return render(request,'b_thietbi_manage.html',context)

def ProjectList(request):
    from .models import Project
    projects = Project.objects.filter(Visibility=True).order_by('Type', 'STT')
    from collections import defaultdict
    project_type = defaultdict(list)
    for project in projects:
        project_type[project.Type].append(project)
    context = {
        'groups':dict(project_type)
    }
    return render(request,'projects.html',context)

@login_required
def ProjectManage(request):
    from .models import Project
    projects = Project.objects.order_by('Type', 'STT')
    from collections import defaultdict
    project_type = defaultdict(list)
    for project in projects:
        project_type[project.Type].append(project)
    context = {
        'groups':dict(project_type)
    }
    return render(request,'project_manage.html',context)

def PhepThuList(request):
    from .models import PhepThu
    phepthus = PhepThu.objects.order_by('Nhom','STT')
    from collections import defaultdict
    phepthu_type = defaultdict(list)
    for phepthu in phepthus:
        phepthu_type[phepthu.Nhom].append(phepthu)
    context = {
        'groups':dict(phepthu_type)
    }
    return render(request,'b_phepthu.html',context)

@login_required
def PhepThuManage(request):
    from .models import PhepThu
    phepthus = PhepThu.objects.order_by('Nhom','STT')
    from collections import defaultdict
    phepthu_type = defaultdict(list)
    for phepthu in phepthus:
        phepthu_type[phepthu.Nhom].append(phepthu)
    context = {
        'groups':dict(phepthu_type)
    }
    return render(request,'b_phepthu_manage.html',context)

def NewsList(request):
    from .models import News
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    news = News.objects.filter(Visibility=True)
    page = request.GET.get('page', 1)
    paginator_1 = Paginator(news, 10)
    try:
        news_page = paginator_1.page(page)
    except PageNotAnInteger:
        news_page = paginator_1.page(1)
    except EmptyPage:
        news_page = paginator_1.page(paginator_1.num_pages)
    context={
        'page':news_page
    }
    return render(request,'news.html',context)

def NewsDetail(request,slug):
    from .models import News
    from django.shortcuts import get_object_or_404
    ins = get_object_or_404(News, slug=slug)
    print(ins)
    context = {
        'i':ins
    }
    return render(request,'newsdetail.html',context)

def Contact(request):
    context={}
    return render(request,'contact.html',context)


#_______FUNCTION_______________________________________________________________


#_______API____________________________________________________________________
def Contact_submit(request):
    from .models import Contact
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        content = request.POST.get('content')

        # Kiểm tra dữ liệu cơ bản
        if fullname and phone and email:
            # Lưu vào MySQL
            Contact.objects.create(
                fullname=fullname,
                phone=phone,
                email=email,
                content=content
            )
            return JsonResponse({'status': 'success', 'message': 'Gửi thành công!'})
        
        return JsonResponse({'status': 'error', 'message': 'Vui lòng điền đủ thông tin.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Yêu cầu không hợp lệ.'}, status=400)

from django.views.decorators.http import require_POST
from django.db import transaction

@login_required
@require_POST
def Reorder_nhansu(request):
    ids = request.POST.getlist('ids[]')
    from .models import HR
    with transaction.atomic():
        for index, pk in enumerate(ids):
            HR.objects.filter(pk=pk).update(STT=index + 1)

    return JsonResponse({'status': 'ok'})

# NHAN SU EDIT API
@login_required
def get_hr_files(request, pk):
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from .models import HR, Degree, HopDong
    hr = get_object_or_404(HR, pk=pk)
    hr = get_object_or_404(HR, pk=pk)
    # Sử dụng list comprehension để lấy url đầy đủ của file
    degrees = [
        {
            'id': d.id,
            'Name': d.Name,
            'File': d.File.url if d.File else '' # d.File.url sẽ trả về dạng /media/path/to/file.pdf
        } for d in Degree.objects.filter(Owner=hr)
    ]
    
    contracts = [
        {
            'id': c.id,
            'File': c.File.url if c.File else ''
        } for c in HopDong.objects.filter(NguoiKy=hr)
    ]
    
    return JsonResponse({'degrees': degrees, 'contracts': contracts})

@login_required
def update_hr_full(request):
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from .models import HR, Degree, HopDong
    from django.db.models import Max
    from django.utils.text import slugify
    if request.method == 'POST':
        hr_id = request.POST.get('id')
        # hr = get_object_or_404(HR, id=hr_id)
        if hr_id: # CHẾ ĐỘ CHỈNH SỬA
            hr = get_object_or_404(HR, id=hr_id)
        else: # CHẾ ĐỘ THÊM MỚI
            # Tự động tính STT cao nhất
            max_stt = HR.objects.all().aggregate(Max('STT'))['STT__max'] or 0
            hr = HR(STT=max_stt + 1)
        
        # 1. Cập nhật thông tin cơ bản HR
        hr.Name = request.POST.get('Name')
        hr.Sex = request.POST.get('Sex')
        hr.BirthYear = request.POST.get('BirthYear')
        hr.Experience = request.POST.get('Experience')
        hr.Degree = request.POST.get('Degree')
        hr.Title = request.POST.get('Title')
        hr.Note = request.POST.get('Note')
        hr.Visibility = request.POST.get('Visibility') == 'on' # Checkbox xử lý 'on'/'off'
        hr.Unit = request.POST.get('Unit') # Thêm Unit
        # Tạo slug tự động từ tên nếu là thêm mới
        if not hr_id:
            hr.slug = slugify(hr.Name) # Đảm bảo bạn đã import slugify
        
        if 'Photo' in request.FILES:
            hr.Photo = request.FILES['Photo']
        hr.save()

        # 2. Xóa các file cũ nếu được tích chọn xóa
        del_degrees = request.POST.getlist('del_degrees')
        Degree.objects.filter(id__in=del_degrees, Owner=hr).delete()
        
        del_contracts = request.POST.getlist('del_contracts')
        HopDong.objects.filter(id__in=del_contracts, NguoiKy=hr).delete()

        # 3. Lưu file mới tải lên (nếu có)
        for f in request.FILES.getlist('new_degrees'):
            Degree.objects.create(Owner=hr, File=f, Name=f.name, Type='Bằng cấp')
        
        for f in request.FILES.getlist('new_contracts'):
            HopDong.objects.create(NguoiKy=hr, File=f)

        return JsonResponse({'status': 'success', 'message': 'Cập nhật hồ sơ thành công!'})
    

@login_required
def delete_hr_photo(request, pk):
    from .models import HR
    import os
    from django.conf import settings
    if request.method == 'POST':
        hr = get_object_or_404(HR, pk=pk)
        if hr.Photo:
            # Xóa file vật lý trong thư mục media
            if os.path.isfile(hr.Photo.path):
                os.remove(hr.Photo.path)
            # Xóa bản ghi trong database
            hr.Photo = None
            hr.save()
            return JsonResponse({'status': 'success', 'message': 'Đã xóa ảnh thành công'})
    return JsonResponse({'status': 'error', 'message': 'Thao tác không hợp lệ'}, status=400)


@login_required
@require_POST
def delete_personnel(request, pk):
    from django.db.models import F
    from django.db import transaction
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    from .models import HR
    if request.method == 'POST':
        hr = get_object_or_404(HR, pk=pk)
        stt_deleted = hr.STT

        try:
            # Sử dụng transaction để đảm bảo nếu lỗi thì không xóa và không cập nhật STT
            with transaction.atomic():
                # 1. Xóa nhân sự
                hr.delete()

                # 2. Cập nhật STT cho các người còn lại: Giảm 1 đơn vị cho những ai có STT lớn hơn người vừa xóa
                HR.objects.filter(STT__gt=stt_deleted).update(STT=F('STT') - 1)

            return JsonResponse({'status': 'success', 'message': 'Đã xóa và cập nhật STT thành công!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

# 1. Cập nhật hoặc Thêm mới Thiết bị
@login_required
def update_thietbi_full(request):
    from django.shortcuts import render, get_object_or_404
    from django.http import JsonResponse
    from django.db.models import F, Max
    from django.db import transaction
    from .models import ThietBi, HieuChuan
    if request.method == 'POST':
        tb_id = request.POST.get('id')
        
        try:
            with transaction.atomic():
                if tb_id:  # Chế độ Chỉnh sửa
                    tb = get_object_or_404(ThietBi, id=tb_id)
                else:      # Chế độ Thêm mới
                    # Tính STT tự động: lấy số lớn nhất hiện tại + 1
                    max_stt = ThietBi.objects.all().aggregate(Max('STT'))['STT__max'] or 0
                    tb = ThietBi(STT=max_stt + 1)

                # Gán dữ liệu từ form
                tb.Ten = request.POST.get('Ten')
                tb.Nhom = request.POST.get('Nhom')
                tb.NhanHieu = request.POST.get('NhanHieu')
                tb.SoLuong = request.POST.get('SoLuong', 1)
                tb.TinhTrang = request.POST.get('TinhTrang')
                tb.GhiChu = request.POST.get('GhiChu')
                tb.Visibility = request.POST.get('Visibility') == 'on'

                if 'HinhAnh' in request.FILES:
                    tb.HinhAnh = request.FILES['HinhAnh']
                
                tb.save()

                # Xử lý xóa các file Hiệu chuẩn được tích chọn
                del_hieuchuan_ids = request.POST.getlist('del_hieuchuan')
                if del_hieuchuan_ids:
                    HieuChuan.objects.filter(id__in=del_hieuchuan_ids).delete()

                # Xử lý thêm các file Hiệu chuẩn mới
                new_files = request.FILES.getlist('new_hieuchuan_files')
                for f in new_files:
                    HieuChuan.objects.create(
                        May=tb,
                        File=f,
                        Ten=f.name # Lấy tên file gốc làm tên hiển thị tạm thời
                    )

            return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# 2. Xóa thiết bị và tự động cập nhật lại STT
@login_required
def delete_thietbi(request, pk):
    from django.shortcuts import render, get_object_or_404
    from django.http import JsonResponse
    from django.db.models import F, Max
    from django.db import transaction
    from .models import ThietBi, HieuChuan
    if request.method == 'POST':
        tb = get_object_or_404(ThietBi, pk=pk)
        stt_deleted = tb.STT
        
        try:
            with transaction.atomic():
                tb.delete()
                # Cập nhật STT: Những thiết bị có STT lớn hơn máy vừa xóa sẽ giảm đi 1
                ThietBi.objects.filter(STT__gt=stt_deleted).update(STT=F('STT') - 1)
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# 3. Lấy danh sách file hiệu chuẩn (Dùng cho Modal Edit)
@login_required
def get_hieuchuan_files(request, pk):
    from django.shortcuts import render, get_object_or_404
    from django.http import JsonResponse
    from django.db.models import F, Max
    from django.db import transaction
    from .models import ThietBi, HieuChuan
    tb = get_object_or_404(ThietBi, pk=pk)
    # Lấy danh sách hồ sơ, nếu không có sẽ trả về QuerySet rỗng chứ không lỗi
    files = HieuChuan.objects.filter(May=tb)
    
    data = []
    for f in files:
        # Kiểm tra file vật lý tồn tại mới lấy URL
        file_url = f.File.url if f.File else None
        if file_url:
            data.append({
                'id': f.id,
                'Ten': f.Ten or "Hồ sơ hiệu chuẩn",
                'File': file_url
            })
    return JsonResponse({'files': data})



# API PHÉP THỬ
from django.db.models import F, Max
from .models import PhepThu

# 1. Cập nhật hoặc Thêm mới Phép thử
@login_required
def update_phepthu_full(request):
    if request.method == 'POST':
        pt_id = request.POST.get('id')
        nhom_moi = request.POST.get('Nhom')
        
        with transaction.atomic():
            if pt_id:
                pt = get_object_or_404(PhepThu, id=pt_id)
                # Nếu đổi nhóm, cần đánh lại STT ở nhóm cũ và gán STT mới ở nhóm mới
                if pt.Nhom != nhom_moi:
                    # Giảm STT các phép thử ở nhóm cũ
                    PhepThu.objects.filter(Nhom=pt.Nhom, STT__gt=pt.STT).update(STT=F('STT') - 1)
                    # Lấy STT cao nhất ở nhóm mới
                    max_stt = PhepThu.objects.filter(Nhom=nhom_moi).aggregate(Max('STT'))['STT__max'] or 0
                    pt.STT = max_stt + 1
            else:
                # Thêm mới: Lấy STT cao nhất của nhóm đó
                max_stt = PhepThu.objects.filter(Nhom=nhom_moi).aggregate(Max('STT'))['STT__max'] or 0
                pt = PhepThu(STT=max_stt + 1)

            pt.Ten = request.POST.get('Ten')
            pt.Nhom = nhom_moi
            pt.TCKT = request.POST.get('TCKT')
            pt.Note = request.POST.get('Note')
            pt.save()

        return JsonResponse({'status': 'success'})

# 2. Xóa phép thử và dồn STT trong nhóm
@login_required
def delete_phepthu(request, pk):
    if request.method == 'POST':
        pt = get_object_or_404(PhepThu, pk=pk)
        nhom = pt.Nhom
        stt_deleted = pt.STT
        with transaction.atomic():
            pt.delete()
            # Chỉ giảm STT của những phép thử CÙNG NHÓM
            PhepThu.objects.filter(Nhom=nhom, STT__gt=stt_deleted).update(STT=F('STT') - 1)
        return JsonResponse({'status': 'success'})
    
# sắp xếp phép thử
@login_required
@require_POST
def update_phepthu_order(request):
    from .models import PhepThu
    ids = request.POST.getlist('ids[]')
    nhom_ten = request.POST.get('nhom') # Nhận tên nhóm từ JS
    
    if not ids or not nhom_ten:
        return JsonResponse({'status': 'error', 'message': 'Thiếu dữ liệu'}, status=400)

    try:
        with transaction.atomic():
            # Chỉ cập nhật STT cho các phép thử thuộc đúng nhóm đang kéo thả
            # enumerate(ids, start=1) sẽ tạo ra thứ tự 1, 2, 3... cho nhóm đó
            for index, pt_id in enumerate(ids, start=1):
                PhepThu.objects.filter(id=pt_id, Nhom=nhom_ten).update(STT=index)
                
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
# api dự án 

# 1. Cập nhật hoặc Thêm mới Dự án
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.db.models import F, Max
from .models import Project

# View xử lý Thêm/Sửa
@login_required
def update_project_full(request):
    if request.method == 'POST':
        p_id = request.POST.get('id')
        type_moi = request.POST.get('Type')
        
        try:
            with transaction.atomic():
                if p_id: # Trường hợp SỬA
                    p = get_object_or_404(Project, id=p_id)
                    # Nếu đổi nhóm, phải đánh lại STT nhóm cũ và lấy STT mới ở nhóm mới
                    if p.Type != type_moi:
                        Project.objects.filter(Type=p.Type, STT__gt=p.STT).update(STT=F('STT') - 1)
                        max_stt = Project.objects.filter(Type=type_moi).aggregate(Max('STT'))['STT__max'] or 0
                        p.STT = max_stt + 1
                else: # Trường hợp THÊM MỚI
                    max_stt = Project.objects.filter(Type=type_moi).aggregate(Max('STT'))['STT__max'] or 0
                    p = Project(STT=max_stt + 1)

                # Gán dữ liệu chung
                p.Name = request.POST.get('Name')
                p.Type = type_moi
                p.Investor = request.POST.get('Investor')
                p.Job = request.POST.get('Job')
                p.FundBy = request.POST.get('FundBy')
                p.Progress = request.POST.get('Progress')
                p.Visibility = True if request.POST.get('Visibility') == 'on' else False
                p.save()
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# 2. Xóa dự án
@login_required
def delete_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        type_p = project.Type
        stt_deleted = project.STT
        
        try:
            with transaction.atomic():
                # Xóa dự án
                project.delete()
                # Cập nhật lại STT: Giảm 1 cho tất cả dự án cùng nhóm có STT lớn hơn dự án vừa xóa
                Project.objects.filter(Type=type_p, STT__gt=stt_deleted).update(STT=F('STT') - 1)
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# manage news
from .models import News
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.shortcuts import render, redirect

# Form để dùng cho trang Thêm/Sửa (vì có CKEditor và Slug)
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['Name', 'Image', 'Description', 'Content', 'Visibility', 'Attachment']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Content': forms.CharField(widget=CKEditorUploadingWidget()),
            'Visibility': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# 1. Trang danh sách quản lý
@login_required
def news_manage(request):
    news_list = News.objects.all().order_by('-Created_at')
    return render(request, 'news_manage.html', {'news_list': news_list})

# 2. Trang Thêm/Sửa (Gộp chung)
@login_required
def news_edit(request, pk=None):
    if pk:
        news_item = get_object_or_404(News, pk=pk)
        title = "Chỉnh sửa tin tức"
    else:
        news_item = None
        title = "Thêm tin tức mới"

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            new_obj = form.save(commit=False)
            if not news_item:
                new_obj.Created_by = request.user
            new_obj.save()
            return redirect('main:news_manage')
    else:
        form = NewsForm(instance=news_item)
    
    return render(request, 'news_edit_form.html', {'form': form, 'title': title})

# 3. API Xóa (Dùng cho Modal)
@login_required
def news_delete(request, pk):
    if request.method == 'POST':
        news_item = get_object_or_404(News, pk=pk)
        news_item.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)