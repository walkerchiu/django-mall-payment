import graphene

from django_app_core.relay.connection import DjangoFilterConnectionField
from django_mall_payment.graphql.storefront.types.payment import PaymentNode


class PaymentMutation(graphene.ObjectType):
    pass


class PaymentQuery(graphene.ObjectType):
    payment = graphene.relay.Node.Field(PaymentNode)
    payments = DjangoFilterConnectionField(
        PaymentNode,
        orderBy=graphene.List(of_type=graphene.String),
        page_number=graphene.Int(),
        page_size=graphene.Int(),
    )
