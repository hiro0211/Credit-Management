from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Subject, Category
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, SiteAuthDataForm
from django.db.models import Sum
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from django.views import generic

class TopView(TemplateView):
  template_name= "top.html"

class SubjectListView(LoginRequiredMixin, ListView):
  model = Subject
  paginate_by = 24

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(*args, **kwargs)

    context["categories"] = Category.objects.all()
    return context
  
  def get_queryset(self):
    query = self.request.GET.get('query')

    if query:
      subject_list = Subject.objects.filter(
            name__icontains=query)
    else:
      subject_list = Subject.objects.all()
    return subject_list

class SubjectCreateView(LoginRequiredMixin, CreateView):
  model = Subject
  fields = '__all__'

class LoadDataFromSite(generic.FormView):
    template_name= "crud/unipa_register.html"
    form_class = SiteAuthDataForm
    def form_valid(self, form):
        user_id = form.cleaned_data['user_id']
        password_text = form.cleaned_data['password']
        # test.pyの内容をこの下に書く
        chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")

        # Chromeドライバーを起動
        #chrome_driver = webdriver.Chrome(chrome_options=chrome_options)

        chrome_driver.get("https://unipa.itp.kindai.ac.jp/up/faces/login/Com00501A.jsp")

        time.sleep(1)

        mail = chrome_driver.find_element(By.ID, 'form1:htmlUserId') 
        password = chrome_driver.find_element(By.ID, 'form1:htmlPassword')

        mail.clear()
        password.clear()

        mail.send_keys(user_id)
        password.send_keys(password_text)

        #mail.submit()
        button = chrome_driver.find_element(By.ID, 'form1:login')
        button.click()

        #chrome_driver.save_screenshot('screenshot.png')
        target_element = chrome_driver.find_element(By.ID, 'menuc3')
        actions = ActionChains(chrome_driver)
        actions.move_to_element(target_element).perform()

        time.sleep(2)
        grade = chrome_driver.find_element(By.ID, 'menuimg3-1')
        grade.click()

        time.sleep(10)
        first_semester = chrome_driver.find_element(By.ID, 'singleTableArea')
        print(first_semester.text)

        subject_element = first_semester.find_element(By.CLASS_NAME, 'tdTaniList')
        print(subject_element)
        subject = subject_element.text
        
        #credit_element = chrome_driver.find_element(By.CLASS_NAME, 'tdKyoshokuinNameList')
        #credit = credit_element.text
        
        return render(self.request, 'total.html', {'subject': subject})
        #chrome_driver.quit()

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
  model = Subject
  fields = '__all__'
  template_name_suffix = '_update_form'

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
  model = Subject
  success_url = reverse_lazy('list')

class SubjectDetailView(LoginRequiredMixin, DetailView):
  model = Subject
  context_object_name = 'subject'
  template_name = "crud/subject_detail.html"

class CategorySubjectListView(ListView):
  model = Subject
  template_name = "crud/category_subject.html"
  context_object_name = "subjects"

  def get_queryset(self, **kwargs):
    category_name = self.kwargs["category"]
    category = get_object_or_404(Category, name=category_name)
    return super().get_queryset().filter(category=category)

class LoginView(LoginView):
  form_class = AuthenticationForm
  template_name ='login.html'
  success_url = reverse_lazy('list')

class LogoutView(LoginRequiredMixin, LogoutView):
  template_name = 'top.html'

class SignUpView(CreateView):
  form_class = SignUpForm
  template_name = "crud/signup.html"
  success_url = reverse_lazy('list')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    self.object = user 
    return HttpResponseRedirect(self.get_success_url())
  
def calculate_total(request):
    total_credit = Subject.objects.aggregate(Sum('credit'))['credit__sum']
    filtered_kyoutu = Subject.objects.filter(category_id = 1)
    kyoutu = filtered_kyoutu.aggregate(Sum('credit'))['credit__sum']
    rest_kyoutu = 16 - kyoutu

    filtered_first = Subject.objects.filter(category_id = 2)
    first_language = filtered_first.aggregate(Sum('credit'))['credit__sum']
    rest_fisrt = 14 - first_language

    filtered_second = Subject.objects.filter(category_id = 3)
    second_language = filtered_second.aggregate(Sum('credit'))['credit__sum']

    filtered_gakubu = Subject.objects.filter(category_id = 4)
    gakubu_subject = filtered_gakubu.aggregate(Sum('credit'))['credit__sum']
    rest_gakubu = 14 - gakubu_subject

    filtered_department = Subject.objects.filter(category_id = 5)
    department_subject = filtered_department.aggregate(Sum('credit'))['credit__sum']
    rest_department = 28 - department_subject 

    filtered_information = Subject.objects.filter(category_id = 7)
    information_subject = filtered_information.aggregate(Sum('credit'))['credit__sum']
    rest_infomation = 8 - information_subject

    filterd_field = Subject.objects.filter(category_id = 6)
    field_subject = filterd_field.aggregate(Sum('credit'))['credit__sum']

    specialize_subject = (gakubu_subject or 0) + (department_subject or 0)+ (field_subject or 0) + (information_subject or 0)
    rest_specialize = 92 - specialize_subject

    foreign_language = first_language + second_language
    rest_foreign = 20 - foreign_language

    # kyoutu = Subject.objects.filter(category_id = 4)
    rest_credit = 128 - total_credit 
    return render(request, 'total.html', {'total_credit': total_credit, 'rest_credit': rest_credit, 'rest_kyoutu': rest_kyoutu, 'rest_first': rest_fisrt, 
                  'rest_gakubu': rest_gakubu, 'rest_department': rest_department, 'rest_information': rest_infomation, 'rest_specialize': rest_specialize,
                  'rest_foreign': rest_foreign})


"""
def graduation_requirements(request):
    #student = Student.objects.get()
    
    # カテゴリーごとの単位を数える
    category_credits = {}
    for category in Category.objects.all():
        category_credits[category.name] = category.subject_set.aggregate(total_credits=Sum('credit'))['total_credits'] or 0
    
    # カテゴリーごとの必要な単位数
    required_credits = {
        '学科共通科目': 10,
        '専門科目': 128,
        # 他のカテゴリーも追加
    }
    
    # 卒業までの残りの単位数
    remaining_credits = {}
    for category, required_credit in required_credits.items():
        remaining_credit = required_credit - category_credits.get(category, 0)
        if remaining_credit > 0:
            remaining_credits[category] = remaining_credit
    
    return render(request, 'total.html', {'remaining_credits': remaining_credits})
"""