from django.urls import path

from store.constants import PRODUCT_SEARCH_VIEW_NAME
from . import views

urlpatterns = [
    path('products/', views.product_search_view, name=PRODUCT_SEARCH_VIEW_NAME),
]
