from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cosine-similarity', views.cosine_similarity, name="cosine-similarity"),
    path('path-length', views.path_length, name="path-length"),
    path('semantic-content-similarity', views.semantic_content_similarity, name="semantic-content-similarity"),
]
