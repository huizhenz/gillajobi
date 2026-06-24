from .utils import generate_embedding, cosine_similarity

# Create your views here.
def search(request):
    query = request.GET.get('q', '')
    query_vec = generate_embedding(query)

    # best_category = max(
    #     Category.objects.all(),
    #     key=lambda c: cosine_similarity(query_vec, generate_embedding(c.name))
    # )