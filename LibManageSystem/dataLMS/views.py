from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView

from dataLMS.models import Books, IssuedBooks

from .forms import LoginForm, RegistrationForm

# Create your views here.
class RegisterView(View):

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        return render(request, 'dataLMS/register.html', {'form':form})
    
    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            
            if User.objects.filter(email=request.POST['email']).exists():
                return render(request, 'dataLMS/register.html', {'form':form, 'error':'Email already exists. Please Log In'})
            
            request.session['email'] = request.POST['email']
            form.save()
            return HttpResponseRedirect(reverse('account'))



class LoginView(View):

    def get(self, request):
        loginForm = LoginForm()
        if 'email' in list(request.session.keys()):
            return HttpResponseRedirect(reverse('account'))
        return render(request, 'dataLMS/login.html', {'form':loginForm})

    def post(self, request):
        loginForm = LoginForm(request.POST or None)
        if loginForm.is_valid():
            request.session['email'] = request.POST['email']
            return HttpResponseRedirect(reverse('account'))

        return render(request, 'dataLMS/login.html', {'form':loginForm, 'error':loginForm.errors})


class BookListView(View):
    def get(self, request):
        books = Books.objects.all()
        if 'email' in request.session.keys():
            return render(request, 'dataLMS/bookList.html', {'books':books, 'data':True})
        return render(request, 'dataLMS/bookList.html', {'books':books})



class BookDetailView(View):

    def get(self, request, slug):
        data = Books.objects.get(slug=slug)
        val = False
        if 'email' in list(request.session.keys()):
            val = True
            if IssuedBooks.objects.filter(issuedBook=Books.objects.get(slug=slug), issuer=User.objects.get(email=request.session['email'])).exists():
                return render(request, 'dataLMS/bookDetail.html', {'object':data, 'return':True, 'data':val})
        return render(request, 'dataLMS/bookDetail.html', {'object':data, 'data':val})
    
    
    def post(self, request, slug):
        try:
            a = IssuedBooks.objects.create(issuer=User.objects.get(email=request.session['email']), issuedBook=Books.objects.get(slug=slug))
                
            return HttpResponseRedirect(reverse('bookDetail', args=[slug]))
        except Exception as e:
            # return HttpResponse(e)
            return HttpResponseRedirect(reverse('login'))

class ReturnBookView(View):
    def post(self, request, slug):
        book_id = slug
        try:
            IssuedBooks.objects.get(issuedBook=Books.objects.get(slug=book_id), issuer=User.objects.get(email=request.session['email'])).delete()
            return HttpResponseRedirect(reverse('bookDetail', args=[book_id]))
        except Exception as e:
            return HttpResponse(e)
            # return HttpResponseRedirect(reverse('login'))

class AccountView(View):

    def get(self, request):
        try:
            object = User.objects.get(email=request.session['email'])
            context= list(IssuedBooks.objects.filter(issuer=User.objects.get(email=request.session['email'])))
            if len(context) == 0:
                context = None
            return render(request, 'dataLMS/account.html', {'object':object, 'bookData':context})
        except Exception as e:
            # return HttpResponse(e)
            return HttpResponseRedirect(reverse('login'))


class LogoutView(View):
    def get(self, request):
        del request.session['email']
        return HttpResponseRedirect(reverse('books'))