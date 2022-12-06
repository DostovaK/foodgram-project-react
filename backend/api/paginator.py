from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Creating a paginator that inherits from PageNumberPagination."""
    page_size = 6
    page_size_query_param = 'limit'
