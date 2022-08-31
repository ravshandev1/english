from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 10
    display_page_controls = 'page_size'
