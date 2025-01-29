import graphene
# from graphql_auth.schema import UserQuery, MeQuery
# from graphql_auth import mutations
import graphql_jwt
from items.schema import ItemsQuery, ItemsMutation

# class AuthMutation(graphene.ObjectType):
#     register = mutations.Register.Field()
#     verify_account = mutations.VerifyAccount.Field()
#     token_auth = mutations.ObtainJSONWebToken.Field()
#     refresh_token = mutations.RefreshToken.Field()
#     revoke_token = mutations.RevokeToken.Field()
  
class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(ItemsQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, ItemsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)