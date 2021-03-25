from django.views.generic import ListView
from django.db.models import Q
from django.utils.http import urlencode

class SearchView(ListView):
    search_form_class=None
    search_fields=[]
    input_name=None


    def get(self,request, **kwargs):
        self.form = self.search_form_class(request.GET)
        self.search_data = self.get_search_data()
        return super(SearchView, self).get(request, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_data:
            queryset = self.model.objects.none()
            for field in self.search_fields:
                objects = queryset.filter(
                    Q(field__icontains=self.search_data)
                )
                for ob in objects:
                    queryset |= self.model.objects.filter(pk=ob.pk)
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data[self.input_name]
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.input_name] = self.form

        if self.search_data:
            context['query'] = urlencode({self.input_name: self.search_data})

        return context
