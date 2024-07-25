from django.views.decorators.cache import cache_control, never_cache


class CacheControlMixin:
    """
    Mixin that allows setting Cache-Control options for Django class-based views.

    This mixin enables specifying various Cache-Control headers as class attributes on the view class.
    The available options include:
    - public: Indicates that the response may be cached by any cache.
    - private: Indicates that the response is intended for a single user and must not be stored by shared caches.
    - no_cache: Forces caches to submit the request to the origin server for validation before releasing a cached copy.
    - no_transform: Prohibits intermediate caches from modifying the response content.
    - must_revalidate: Indicates that once a cached response becomes stale, it must not be used again without successful validation on the origin server.
    - proxy_revalidate: Similar to must_revalidate, but only for shared caches.
    - max_age: Specifies the maximum amount of time a resource is considered fresh.
    - s_maxage: Overrides max_age or the Expires header for shared caches (e.g., proxies).

    Use-Cases:
    - When you need to control how a view's response is cached by browsers and intermediary caches.
    - Useful for views serving static content that can be cached for performance improvement.
    - Applicable in scenarios where cache invalidation and freshness need to be finely managed.

    Example Usage:
    class MyCacheControlledView(CacheControlMixin, TemplateView):
        template_name = 'my_template.html'
        cachecontrol_public = True
        cachecontrol_max_age = 3600  # 1 hour
    """

    cachecontrol_public = None
    cachecontrol_private = None
    cachecontrol_no_cache = None
    cachecontrol_no_transform = None
    cachecontrol_must_revalidate = None
    cachecontrol_proxy_revalidate = None
    cachecontrol_max_age = None
    cachecontrol_s_maxage = None

    @classmethod
    def get_cachecontrol_options(cls):
        """Compile a dictionary of selected cache options"""
        opts = (
            'public', 'private', 'no_cache', 'no_transform',
            'must_revalidate', 'proxy_revalidate', 'max_age',
            's_maxage'
        )
        options = {}
        for opt in opts:
            value = getattr(cls, f'cachecontrol_{opt}', None)
            if value is not None:
                options[opt] = value
        return options

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Wrap the view with appropriate cache controls"""
        view_func = super().as_view(*args, **kwargs)
        options = cls.get_cachecontrol_options()
        return cache_control(**options)(view_func)


class NeverCacheMixin:
    """
    Mixin that applies Django's `never_cache` view decorator to prevent HTTP-based caching.

    This mixin ensures that the response from the view it is applied to will never be cached by setting
    the Cache-Control header to 'no-cache'. This is useful for views that deliver highly dynamic content
    or sensitive data that should not be stored in any cache.

    Use-Cases:
    - When you need to ensure that the content is always fresh and never stored by browsers or intermediary caches.
    - Useful for views serving user-specific data, such as dashboards or forms where data changes frequently.
    - Applicable in scenarios where data privacy and up-to-date content are critical.

    Example Usage:
    class MyNeverCachedView(NeverCacheMixin, TemplateView):
        template_name = 'my_template.html'
    """
    @classmethod
    def as_view(cls, *args, **kwargs):
        """
        Wrap the view with the `never_cache` decorator.
        """
        view_func = super().as_view(*args, **kwargs)
        return never_cache(view_func)
