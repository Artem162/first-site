from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати статтю', 'url_name': 'add_page'},
        {'title': 'Зворотній зв\'язок', 'url_name': 'contact'},
        {'title': 'Увійти', 'url_name': 'login'}
        ]


class DataMixin:
    paginated_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        # cats = Category.objects.all()
        if not cats:
            cats = Category.objects.annotate(Count('movie'))
            cache.set('cats', cats, 30)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
