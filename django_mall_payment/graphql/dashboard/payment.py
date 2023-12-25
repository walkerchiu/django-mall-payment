from django.core.exceptions import ValidationError
from django.db import transaction

from graphene import ResolveInfo
from graphql_relay import from_global_id
import graphene

from django_app_core.decorators import strip_input
from django_app_core.helpers.translation_helper import TranslationHelper
from django_app_core.relay.connection import DjangoFilterConnectionField
from django_mall_payment.graphql.dashboard.types.payment import (
    PaymentNode,
    PaymentTransInput,
)
from django_mall_payment.models import Payment, PaymentTrans


class UpdatePayment(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        sortKey = graphene.Int()
        isPublished = graphene.Boolean()
        publishedAt = graphene.DateTime()
        translations = graphene.List(graphene.NonNull(PaymentTransInput), required=True)

    success = graphene.Boolean()
    payment = graphene.Field(PaymentNode)

    @classmethod
    @strip_input
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input):
        id = input["id"]
        sortKey = input["sortKey"] if "sortKey" in input else None
        isPublished = input["isPublished"] if "isPublished" in input else True
        publishedAt = input["publishedAt"] if "publishedAt" in input else None
        translations = input["translations"]

        translation_helper = TranslationHelper()
        result, message = translation_helper.validate_translations_from_input(
            label="payment", translations=translations
        )
        if not result:
            raise ValidationError(message)

        try:
            _, payment_id = from_global_id(id)
        except:
            raise ValidationError("Bad Request!")

        try:
            payment = Payment.objects.get(pk=payment_id)
            payment.sort_key = sortKey
            payment.is_published = isPublished
            payment.published_at = publishedAt
            payment.save()

            for translation in translations:
                PaymentTrans.objects.update_or_create(
                    payment=payment,
                    language_code=translation["language_code"],
                    defaults={
                        "name": translation["name"],
                        "description": translation["description"],
                        "content_checkout": translation["content_checkout"],
                        "content_checkout_result": translation[
                            "content_checkout_result"
                        ],
                    },
                )
        except Payment.DoesNotExist:
            raise ValidationError("Can not find this payment!")

        return UpdatePayment(success=True, payment=payment)


class PaymentMutation(graphene.ObjectType):
    payment_update = UpdatePayment.Field()


class PaymentQuery(graphene.ObjectType):
    payment = graphene.relay.Node.Field(PaymentNode)
    payments = DjangoFilterConnectionField(
        PaymentNode,
        orderBy=graphene.List(of_type=graphene.String),
        page_number=graphene.Int(),
        page_size=graphene.Int(),
    )
