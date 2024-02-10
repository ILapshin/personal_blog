from typing import Union, List
from django.db.models import Q, QuerySet
from django.core.cache import cache
from rest_framework.request import Request

from blogs.models import BlogPost
from subscriptions.models import Subscription


TIMEOUT = 15 * 60

def get_feed(request: Request) -> Union[QuerySet, List[BlogPost]]:
    """
    Returns feed for a user from cahe or queryes and writes to cache.
    """
    cache_key = f'feed_{request.user.id}'
    query = cache.get(cache_key)

    if not query:
        subscriptions_query = Subscription.objects.filter(subscriber=request.user).values('owner')
        query = BlogPost.objects.prefetch_related(
            'readers'
        ).filter(
            Q(owner__in=subscriptions_query)
        ).exclude(
            readers=request.user
        ).order_by(
            '-created_at'
        )[:500]
        
        cache.set(cache_key, query, timeout=TIMEOUT)
    
    return query