import graphene
from graphene_django.views import GraphQLView


# class MyGraphQLView(GraphQLView):
#     def get_context(self, request):
#         context = super().get_context(request)
#         context['user'] = request.user if request.user.is_authenticated else None
#         return context