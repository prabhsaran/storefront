from django.core.cache import cache
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import DatabaseError
from django.urls.exceptions import NoReverseMatch

from store.models import Product, Category, Tag
from .constants import (
    CATEGORIES_CACHE_KEY,
    PRODUCT_SEARCH_VIEW_NAME,
    TAGS_CACHE_KEY,
    DEFAULT_CACHE_TIMEOUT_SECONDS,
)


def product_search_view(request: HttpRequest) -> HttpResponse:
    """
    Handles the product search and filtering functionality using search, category and tags query parameters.
    The search and filter options can be combined.

    Query Parameters:
        search (str): The search query string to filter products by description.
        category (int): The ID of the category to filter products by category.
        tags (list of int): A list of tag IDs to filter products by tags.
    """
    try:
        # Get query parameters from request
        search_query = request.GET.get('search', '')
        category_id = request.GET.get('category')
        tag_ids = request.GET.getlist('tags')  # Allows multiple tags to be selected

        # Use the custom product manager method to get filtered products
        products_query_set = Product.objects.search_and_filter(
            search_query=search_query, category_id=category_id, tag_ids=tag_ids
        )

        # Get categories and tags from cache or query them if not cached
        categories = cache.get(CATEGORIES_CACHE_KEY)
        if categories is None:
            categories = list(Category.objects.all())
            cache.set(
                CATEGORIES_CACHE_KEY, categories, timeout=DEFAULT_CACHE_TIMEOUT_SECONDS
            )

        tags = cache.get(TAGS_CACHE_KEY)
        if tags is None:
            tags = list(Tag.objects.all())
            cache.set(TAGS_CACHE_KEY, tags, timeout=DEFAULT_CACHE_TIMEOUT_SECONDS)

        # generate the URL to clear filters
        clear_filters_url = reverse(PRODUCT_SEARCH_VIEW_NAME)

    except DatabaseError as e:
        # Handle any database-related errors by providing fallback data and logging the error
        products_query_set = []
        categories = []
        tags = []
        clear_filters_url = "#"
        print(f"Database error: {e}")

    except NoReverseMatch as e:
        # Fallback to the current URL path without any query parameters
        clear_filters_url = request.path
        print(f"URL resolution error for clear filters URL: {e}")

    # Pass products, categories, and tags to the html template
    page_context = {
        'products': list(products_query_set),  # Evaluate the queryset
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_tags': tag_ids,
        'clear_filters_url': clear_filters_url,  # View URL without query parameters to clear filters
    }

    return render(request, 'product_list.html', page_context)
