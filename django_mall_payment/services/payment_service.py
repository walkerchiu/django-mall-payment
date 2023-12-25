from typing import List, Tuple

from django.db import transaction

from django_app_organization.models import Organization
from django_mall_payment.models import Payment


class PaymentService:
    @transaction.atomic
    def init_default_data(
        self, organization: Organization
    ) -> Tuple[bool, List[Payment]]:
        items = [
            {
                "slug": "bank-transfer",
                "sort_key": 1,
                "translations": [
                    {"language_code": "zh-TW", "name": "銀行轉帳"},
                    {"language_code": "en", "name": "Bank Transfer"},
                ],
            },
            {
                "slug": "cash-on-pickup",
                "sort_key": 2,
                "translations": [
                    {"language_code": "zh-TW", "name": "門市取貨付款"},
                    {"language_code": "en", "name": "Cash on Pickup"},
                ],
            },
        ]

        results = []
        for item in items:
            payment, created = Payment.objects.get_or_create(
                organization=organization, slug=item["slug"], sort_key=item["sort_key"]
            )
            payment.is_published = True
            payment.save()

            if created:
                for translation in item["translations"]:
                    payment.translations.create(
                        language_code=translation["language_code"],
                        name=translation["name"],
                    )

                results.append(payment)

        return created, results
