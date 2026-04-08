from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
# Create your models here.

class News(models.Model):
    Name = models.TextField()
    Image = models.ImageField(upload_to='NewsImg',blank=True,null=True)
    Description = models.TextField()
    Content = RichTextUploadingField()
    Created_by = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Note = models.TextField(blank=True,null=True)
    Visibility = models.BooleanField(default=True)
    Attachment = models.FileField(blank=True,null=True)
    slug = models.SlugField(blank=True,unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name

from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

current_year = datetime.date.today().year

year = models.IntegerField(
    validators=[
        MinValueValidator(1900),
        MaxValueValidator(current_year)
    ]
)

class HR(models.Model):
    Name = models.CharField(max_length=200)
    STT = models.IntegerField()
    Sex = models.CharField(max_length=20,default='Nam',choices=(('Nam','Nam'),('Nữ','Nữ')))
    BirthYear = models.IntegerField()
    Experience = models.PositiveIntegerField()
    Degree = models.CharField(max_length=200)
    Title = models.CharField(max_length=200)
    Note = models.TextField(blank=True,null=True)
    Visibility = models.BooleanField(default=True)
    Photo = models.ImageField(blank=True,null=True,upload_to='NhanSu')
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    Unit = models.CharField(max_length=100,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Tạo slug cơ bản ban đầu
            base_slug = slugify(self.Name)
            slug = base_slug
            count = 1
            
            # Vòng lặp kiểm tra: nếu slug đã tồn tại thì tăng số thứ tự
            while HR.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.STT} - {self.Name}'
    
class Degree(models.Model):
    Type = models.CharField(max_length=100,choices=(('Bằng cấp','Bằng cấp'),('Chứng chỉ','Chứng chỉ')))
    Name = models.CharField(max_length=250)
    Date = models.DateField(blank=True,null=True)
    Owner = models.ForeignKey(HR,on_delete=models.SET_NULL,null=True)
    File = models.FileField(upload_to='degree/')

    def __str__(self):
        return f'{self.Owner} - {self.Type} - {self.Name}'

class Project(models.Model):
    project_type = (
        ('TƯ VẤN KIỂM ĐỊNH, THÍ NGHIỆM','TƯ VẤN KIỂM ĐỊNH, THÍ NGHIỆM'),
        ('TƯ VẤN THÍ NGHIỆM, KIỂM ĐỊNH, KHẢO SÁT ĐỊA CHẤT','TƯ VẤN THÍ NGHIỆM, KIỂM ĐỊNH, KHẢO SÁT ĐỊA CHẤT'),
        ('TƯ VẤN THIẾT KẾ, LẬP DỰ ÁN','TƯ VẤN THIẾT KẾ, LẬP DỰ ÁN'),
        ('TƯ VẤN THẨM TRA AN TOÀN GIAO THÔNG, THIẾT KẾ','TƯ VẤN THẨM TRA AN TOÀN GIAO THÔNG, THIẾT KẾ')
    )
    Name = models.TextField()
    Type = models.CharField(max_length=200,blank=True,null=True,choices=project_type)
    STT = models.IntegerField()
    Year = models.PositiveIntegerField(blank=True,null=True)
    Investor = models.CharField(max_length=250)
    Job = models.TextField()
    FundBy = models.CharField(max_length=200)
    Progress = models.CharField(choices=(('Đang thực hiện','Đang thực hiện'),('Đã hoàn thành','Đã hoàn thành')),max_length=100)
    Visibility = models.BooleanField(default=True)
    Note = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.STT} - {self.Name}'



class PhepThu(models.Model):
    Ten = models.CharField(max_length=500)
    STT = models.IntegerField()
    Nhom = models.CharField(max_length=500)
    TCKT = models.TextField()
    Note = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.STT} - {self.Ten}'

class ThietBi(models.Model):
    STT = models.IntegerField()
    Ten = models.CharField(max_length=500)
    Nhom = models.CharField(max_length=250,blank=True,null=True)
    NhanHieu = models.CharField(max_length=250,blank=True,null=True)
    SoLuong = models.IntegerField(default=1)
    TinhTrang = models.CharField(max_length=250,blank=True,null=True)
    Visibility = models.BooleanField(default=True)
    HieuChuan = models.FileField(upload_to='HieuChuan',blank=True,null=True)
    HinhAnh = models.ImageField(upload_to='AnhThietBi',blank=True,null=True)
    GhiChu = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'{self.STT} - {self.Ten} - {self.Nhom}'
    
class Contact(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="Họ và tên")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")

    def __str__(self):
        return f"{self.fullname} - {self.phone}"
