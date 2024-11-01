from typing import Iterable
from django.db import models
from django.db.models import Q
from django.core.cache import cache
from django.core.validators import MinValueValidator

from .constants import CATEGORIES_CACHE_KEY, TAGS_CACHE_KEY


class ProductManager(models.Manager):
    """
    Custom manager for the Product model to handle complex queries.
    """

    def search_and_filter(
        self, search_query=None, category_id=None, tag_ids=None
    ) -> models.QuerySet:
        """
        Filters and searches products based on the provided criteria.

        Args:
            search_query (str, optional): A string containing search terms to filter products by their description.
            category_id (int, optional): An integer representing the category ID to filter products by category.
            tag_ids (list of int, optional): A list of integers representing tag IDs to filter products by tags.

        Returns:
            models.QuerySet: A QuerySet of products filtered and sorted based on the provided criteria.
        """

        # Start with all products
        # - prefetch_related('tags') and select_related('category') to load all related tags and category
        #   in a single query, reducing database hits
        products = (
            self.get_queryset()
            .prefetch_related('tags')
            .select_related('category')
            .order_by('title')
        )

        # Apply search filter on description with any word order
        if search_query:
            search_words = (
                search_query.split()
            )  # Split the search query into individual words
            query = Q()
            for word in search_words:
                query &= Q(description__icontains=word)  # Add a filter for each word
            products = products.filter(query)

        # Apply category filter
        if category_id:
            products = products.filter(category_id=category_id)

        # Apply exact match tags filter (product must match all tags)
        if tag_ids:
            for tag_id in tag_ids:
                products = products.filter(tags__id=tag_id)

        return products


class Category(models.Model):
    """
    Category model representing a product category in the store.

    Attributes:
        title (CharField): The title of the category.
        slug (SlugField): A unique slug for the category to be used in URLs alongside product URLS for SEO.
        description (TextField): A description of the category.
        created_at (DateTimeField): The date and time when the category was created.
        updated_at (DateTimeField): The date and time when the category was last updated.

    Methods:
        __str__(): Returns the string representation of the category.
        save(*args, **kwargs): Saves the category and clears the category cache.
        delete(*args, **kwargs): Deletes the category and clears the category cache.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(CATEGORIES_CACHE_KEY)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(CATEGORIES_CACHE_KEY)


class Tag(models.Model):
    """
    Represents a Tag model for storing tag information.

    Attributes:
        label (CharField): The label of the tag, must be unique and have a maximum length of 255 characters.
        created_at (DateTimeField): The date and time when the tag was created, automatically set on creation.
        updated_at (DateTimeField): The date and time when the tag was last updated, automatically set on update.

    Methods:
        __str__(): Returns the string representation of the tag, which is its label.
        save(*args, **kwargs): Saves the tag instance and clears the cache.
        delete(*args, **kwargs): Deletes the tag instance and clears the cache.
    """

    label = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.label

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(TAGS_CACHE_KEY)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(TAGS_CACHE_KEY)


class Product(models.Model):
    """
    Product model representing an item in the store.

    Attributes:
        objects (ProductManager): Custom manager for the Product model.
        title (str): The title of the product.
        slug (str): A unique slug for the product to be used in URLs.
        description (str): A breif description of the product, indexed for search queries.
        unit_price (Decimal): The price per unit of the product, with a minimum value of $1.
        inventory (int): The number of items available in stock, with a minimum value of 0.
        created_at (datetime): The date and time when the product was created.
        updated_at (datetime): The date and time when the product was last updated.
        is_active (bool): A flag indicating whether the product is active. Allows to deactive products without deleting them.
        category (Category): The category to which the product belongs.
        tags (Tag): A list of tags associated with the product.
    """

    objects = ProductManager()
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(db_index=True)  # Indexed for search queries
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)],  # Minimum price of $1
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.title
