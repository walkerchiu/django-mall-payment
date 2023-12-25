from django_filters import CharFilter, FilterSet, OrderingFilter
from graphene import ResolveInfo
from graphene_django import DjangoListField, DjangoObjectType
import graphene
import graphene_django_optimizer as gql_optimizer

from django_app_core.relay.connection import ExtendedConnection
from django_app_core.types import TransTypeInput
from django_mall_payment.models import Payment, PaymentTrans


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ()


class PaymentTransType(DjangoObjectType):
    class Meta:
        model = PaymentTrans
        fields = (
            "language_code",
            "name",
            "description",
            "content_checkout",
            "content_checkout_result",
        )


class PaymentTransInput(TransTypeInput):
    content_checkout = graphene.String()
    content_checkout_result = graphene.String()


class PaymentFilter(FilterSet):
    slug = CharFilter(field_name="slug", lookup_expr="exact")

    class Meta:
        model = Payment
        fields = []

    order_by = OrderingFilter(
        fields=(
            "slug",
            "sort_key",
            "created_at",
            "updated_at",
        )
    )


class PaymentConnection(graphene.relay.Connection):
    class Meta:
        node = PaymentType


class PaymentNode(gql_optimizer.OptimizedDjangoObjectType):
    class Meta:
        model = Payment
        exclude = (
            "deleted",
            "deleted_by_cascade",
        )
        filterset_class = PaymentFilter
        interfaces = (graphene.relay.Node,)
        connection_class = ExtendedConnection

    translations = DjangoListField(PaymentTransType)

    @classmethod
    def get_queryset(cls, queryset, info: ResolveInfo):
        return queryset.prefetch_related("translations")

    @classmethod
    def get_node(cls, info: ResolveInfo, id):
        return cls._meta.model.objects.filter(pk=id).first()

    @staticmethod
    def resolve_translations(root: Payment, info: ResolveInfo):
        return root.translations
