import graphene

from django_mall_payment.graphql.dashboard.payment import PaymentMutation, PaymentQuery


class Mutation(
    PaymentMutation,
    graphene.ObjectType,
):
    pass


class Query(
    PaymentQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
