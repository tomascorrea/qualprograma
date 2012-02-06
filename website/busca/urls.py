from django.conf.urls.defaults import *

from views import SearchView
from forms import SearchForm


from haystack.views import search_view_factory

urlpatterns = patterns('',
    url(r'^$', search_view_factory(
        view_class=SearchView,
        template='busca/busca.html',
        form_class=SearchForm
    ), name='busca'),
)