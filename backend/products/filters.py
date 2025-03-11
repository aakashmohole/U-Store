import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Product.objects.values_list('category', flat=True).distinct(),
                                                field_name="category", lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')  # Min price filter
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')  # Max price filter
    in_stock = django_filters.BooleanFilter(field_name="stock", lookup_expr='gt', method="filter_stock")

    def filter_stock(self, queryset, name, value):
        return queryset.filter(stock__gt=0) if value else queryset

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']
