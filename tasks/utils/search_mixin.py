from django.db.models import Q


class SearchMixin:
    search_param = "q"
    search_fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get(self.search_param, "").strip()

        if not search_query:
            return queryset

        filters = Q()
        for field in self.search_fields:
            filters |= Q(**{f"{field}__icontains": search_query})

        return queryset.filter(filters).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get(
            self.search_param, ""
        ).strip()
        return context

