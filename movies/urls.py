from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(30)(MovieHome.as_view()), name='home'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('logout/', logout_user, name='logout'),
    path('category/<slug:cat_slug>/', MovieCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),

    # path('', index, name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    # path('contact/', contact, name='contact'),
    # path('login/', login, name='login'),
    # path('post/<slug:post_slug>', show_post, name='post'),
    # path('category/<int:cat_id>', show_category, name='category')

    # path('cats/<slug:catid>/', categories),
    # path('archive/<slug:year>/', archive)
]
