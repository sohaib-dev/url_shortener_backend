from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .encode_api import EncodeURL
from .decode_api import DecodeURL

urlpatterns = [
    path('encode/', EncodeURL.as_view()),
    path('decode/', DecodeURL.as_view()),
    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
