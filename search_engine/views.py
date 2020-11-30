import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from search_engine.cosine_similarity import get_child_entity, get_wordnet, get_query_vector, get_cosine_similarity
from search_engine.semantic_content_similarity import get_semantic_content_similarity, get_pah_length_similarity
from search_engine.utils import get_score


def index(request):
    with open('./data/ontology.json', "r") as json_data:
        ontology = json.load(json_data)
    return render(request, 'search_engine/index.html', {
        "ontology": json.dumps(ontology)
    })


@csrf_exempt
def cosine_similarity(request):
    if request.is_ajax() and request.method == "POST":
        entities = json.loads(request.POST['data'])
        entities = get_child_entity(entities)
        wordnet_types = get_wordnet(entities)
        wordnet_vector = get_query_vector(wordnet_types)
        similarities = get_cosine_similarity(wordnet_vector)

        return JsonResponse({'response': json.loads(get_score(similarities))})
    return JsonResponse({"error": "GET Method forbidden"}, status=400)


@csrf_exempt
def path_length(request):
    if request.is_ajax() and request.method == "POST":
        entities = json.loads(request.POST['data'])
        similarities = get_pah_length_similarity(entities)

        return JsonResponse({'response': json.loads(get_score(similarities))})
    return JsonResponse({"error": "GET Method forbidden"}, status=400)


@csrf_exempt
def semantic_content_similarity(request):
    if request.is_ajax() and request.method == "POST":
        entities = json.loads(request.POST['data'])
        similarities = get_semantic_content_similarity(entities)

        return JsonResponse({'response': json.loads(get_score(similarities))})
    return JsonResponse({"error": "GET Method forbidden"}, status=400)
