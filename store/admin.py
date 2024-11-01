"""
Admin configuration for the store app models. Registers models
with custom admin options to enhance the admin interface for better usability:
- Configures display fields, search capabilities, and filters.
- Uses `prepopulated_fields` for slug generation based on titles in relevant models.
"""

from django.contrib import admin
from store.models import Product, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin view for Category model.
    - Displays category title, slug, description, and creation date.
    - Enables search by title and auto-fills slug field based on title.
    """

    list_display = ['title', 'description', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin view for Tag model.
    - Displays tag label and creation date.
    - Enables search by label.
    """

    list_display = ['label', 'created_at']
    search_fields = ['label']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin view for Product model.
    - Configures display fields for product.
    - Provides filtering by category, and search by title and description.
    - Uses autocomplete for category and tags fields and prepopulates slug.
    """

    list_display = [
        'title',
        'description',
        'unit_price',
        'category',
        'inventory',
        'is_active',
        'display_tags',  # Custom method to display all tags for each product
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category']
    autocomplete_fields = ['category', 'tags']
    list_select_related = ['category']
    search_fields = ['title', 'description']

    def get_queryset(self, request):
        """Optimize tag retrieval by prefetching related tags."""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('tags')

    def display_tags(self, obj):
        """Returns a comma-separated list of tags for a product."""
        return ", ".join(tag.label for tag in obj.tags.all())

    display_tags.short_description = 'Tags'  # Sets column header in the admin interface
