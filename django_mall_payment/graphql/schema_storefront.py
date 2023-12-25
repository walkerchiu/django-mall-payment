import graphene

from django_mall_payment.graphql.storefront.payment import PaymentQuery


class Mutation(
    graphene.ObjectType,
):
    pass


class Query(
    PaymentQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
