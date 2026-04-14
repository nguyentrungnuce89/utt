from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def HomePage(request):
    context = {}
    return render(request,'homepage.html',context)

def About(request):
    context = {}
    return render(request,'about.html',context)

def Nhansu(request):
    from .models import HR
    nhansu = HR.objects.filter(Visibility=True)
    context = {
        'nhansu':nhansu
    }
    return render(request,'a_nhansu.html',context)

@login_required
def NhansuManage(request):
    from .models import HR
    nhansu = HR.objects.all()
    context = {
        'nhansu':nhansu
    }
    return render(request,'a_nhansu_manage.html',context)

def NhansuDetail(request,slug):
    from .models import HR,Degree
    member = get_object_or_404(HR, slug=slug)
    degrees = Degree.objects.filter(Owner=member).order_by('-Date')

    context = {
        'i':member,
        'degrees': degrees,
    }
    return render(request,'nhansu_detail_new.html',context)

def Dkkd(request):
    context = {}
    return render(request,'a_dkkd.html',context)

def Hdxd(request):
    context = {}
    return render(request,'a_hdxd.html',context)

def Lasxd(request):
    context = {}
    return render(request,'a_lasxd.html',context)

def Thietbi(request):
    from .models import ThietBi
    thietbis = ThietBi.objects.filter(Visibility=True).order_by('Nhom','STT')
    from collections import defaultdict
    nhomthietbi = defaultdict(list)
    for i in thietbis:
        nhomthietbi[i.Nhom].append(i)
    context = {
        'thietbi':dict(nhomthietbi)
    }
    return render(request,'a_thietbi.html',context)

def ThietbiDetail(request,id):
    from .models import ThietBi,HieuChuan
    ins = get_object_or_404(ThietBi,id=id)
    hieuchuan = HieuChuan.objects.filter(May=ins).order_by('-Ngay')
    context = {
        'i':ins,
        'hcs':hieuchuan
    }
    return render(request,'thietbi_detail.html',context)

def Project(request):
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

def PhepThu(request):
    from .models import PhepThu
    phepthus = PhepThu.objects.order_by('Nhom','STT')
    from collections import defaultdict
    phepthu_type = defaultdict(list)
    for phepthu in phepthus:
        phepthu_type[phepthu.Nhom].append(phepthu)
    context = {
        'groups':dict(phepthu_type)
    }
    return render(request,'phepthu.html',context)

def News(request):
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

@require_POST
def Reorder_nhansu(request):
    ids = request.POST.getlist('ids[]')
    from .models import HR
    with transaction.atomic():
        for index, pk in enumerate(ids):
            HR.objects.filter(pk=pk).update(STT=index + 1)

    return JsonResponse({'status': 'ok'})