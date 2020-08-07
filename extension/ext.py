from typing import List, Callable, Tuple, Optional

from middler.cache import sorted_dict_trait
from middler.config import Config
from middler.request import HttpRequest
from middler.response import HttpResponse
from middler.transform import replace_request_path


def _request_shorten_path(request: HttpRequest) -> HttpRequest:
    return replace_request_path(request, r'^/path/(.+?)(/[a-z]+)(/.*)', r'\3')


def _response_same(request: HttpRequest, response: HttpResponse) -> HttpResponse:
    return response


def _cache_traits(request: HttpRequest) -> Tuple:
    return request.method, request.path, request.content, sorted_dict_trait(request.headers)


def _can_be_cached(request: HttpRequest) -> bool:
    return True


"""Mappers applied on every request before further processing"""
request_transformers: List[Callable[[HttpRequest], HttpRequest]] = [
    _request_shorten_path,
]

"""Mappers applied on every response after all"""
response_transformers: List[Callable[[HttpRequest, HttpResponse], HttpResponse]] = [
    _response_same,
]

"""Gets tuple denoting request uniqueness. Requests with same results are treated as the same when caching."""
cache_traits_extractor: Callable[[HttpRequest], Tuple] = _cache_traits

"""Indicates whether particular request should be cached or not"""
cache_predicate: Callable[[HttpRequest], bool] = _can_be_cached

"""Returns custom config overriding defaults and provided args"""
config_builder: Optional[Callable[[...], Config]] = None
