# Create your views here.
from haystack.views import SearchView as BaseSearchView

class SearchView(BaseSearchView):
    def __name__(self):
        return "SearchView"

    def extra_context(self):
        extra = super(SearchView, self).extra_context()

        if self.results == []:
            extra['facets'] = self.form.search().facet_counts()
        else:
            extra['facets'] = self.results.facet_counts()

        return extra
