from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator  # nummering of pages
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404  # HTML things
from django.urls import reverse_lazy  # redirect but better
from django.views.generic import ListView, DetailView, CreateView, FormView  # django classes for rendering web pages
from django.contrib.auth.mixins import LoginRequiredMixin  # class for no login ppl

from movies.forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from movies.models import *
from movies.utils import DataMixin

# Create your views here.


menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати статтю', 'url_name': 'add_page'},
        {'title': 'Зворотній зв\'язок', 'url_name': 'contact'},
        {'title': 'Увійти', 'url_name': 'login'}
        ]


# class based views(CBV) - views прописаний по класам
# - ListView
# - DetailView
# - CreateView

# Міксін клас - це клас для спадкування


# ListView ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
class MovieHome(DataMixin, ListView):
    paginate_by = 4
    model = Movie
    template_name = 'movies/index.html'
    # object_list - стандартна змінна для всіх елементів бази даних
    # context_object_name - для зміни стандартної змінної для всіх елементів бази даних
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # no need in this part due to DataMixin
        # cats = Category.objects.all()

        # context['title'] = 'Головна сторінка'
        # context['menu'] = menu
        # context['cats'] = cats
        # context['cat_selected'] = 0
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Movie.objects.filter(is_published=True).select_related('cat')


# ListView ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
class MovieCategory(DataMixin, ListView):
    paginate_by = 4
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Movie.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        # context['title'] = 'Категорія: ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cat_selected'] = context['posts'][0].cat_id
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# DetailView ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
class ShowPost(DataMixin, DetailView):
    model = Movie
    template_name = 'movies/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = context['post']
        # context['menu'] = menu
        c_def = self.get_user_context(title='post')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# CreateView ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'movies/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Додавання сторінки'
        # context['menu'] = menu
        c_def = self.get_user_context(title='Додавання сторінки')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'movies/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'movies/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'movies/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Зворотній Зв'язок")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


# def index(request):
#     posts = Movie.objects.all()
#     cats = Category.objects.all()
#     context = {'menu': menu,
#                'cats': cats,
#                'title': 'Головна сторінка',
#                'posts': posts,
#                'catselected': ''}
#     return render(request, 'movies/index.html', context=context)


def about(request):
    contact_list = Movie.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'movies/about.html',
                  {
                      'page_obj': page_obj,
                      'menu': menu,
                      'title': 'Сторінка про сайт',
                  })


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'movies/addpage.html',
#                   {
#                       'form': form,
#                       'menu': menu,
#                       'title': 'Додавання статті'})


def contact(request):
    return HttpResponse("Зворотній зв\'язок")


def login(request):
    return HttpResponse("Авторизація")


# def show_post(request, post_slug):
#     post = get_object_or_404(Movie, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id
#     }
#     return render(request, 'movies/post.html', context=context)


# def show_category(request, cat_id):
#     posts = Movie.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     context = {'menu': menu,
#                'cats': cats,
#                'title': 'Головна сторінка',
#                'posts': posts,
#                'catselected': cat_id}
#     return render(request, 'movies/index.html', context=context)


def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Фільми по категоріях</h1>{catid}<p>")


def pageNotFound(request, exception):
    return HttpResponse("<h1>Сторінку не знайдено</h1>")


def archive(request, year):
    if (int(year) > 2023):
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архів по роках</h1>{year}<p>")

# MTV - model (ORM), template, view
