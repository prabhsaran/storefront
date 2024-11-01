CATEGORIES_CACHE_KEY = 'categories'  # Cache key for storing all category data
TAGS_CACHE_KEY = 'tags'  # Cache key for storing all tag data

# Default cache timeout in seconds (1 day), used for caching frequently accessed data
# that rarely changes, like categories and tags.
DEFAULT_CACHE_TIMEOUT_SECONDS = 86400

# URL name for the product search view, used in reverse lookups to avoid hardcoding URLs.
PRODUCT_SEARCH_VIEW_NAME = 'product_search'
