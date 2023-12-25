import uuid

from django.conf import settings
from django.db import models

from safedelete.models import SOFT_DELETE_CASCADE

from django_app_core.models import (
    CommonDateAndSafeDeleteMixin,
    PublishableModel,
    TranslationModel,
)
from django_app_organization.models import Organization


class Payment(CommonDateAndSafeDeleteMixin, PublishableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, models.CASCADE)
    slug = models.CharField(max_length=255, db_index=True)
    sort_key = models.IntegerField(db_index=True, null=True)

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = settings.APP_NAME + "_payment_payment"
        get_latest_by = "updated_at"
        index_together = [
            ["organization", "slug"],
        ]
        unique_together = [["organization", "slug"]]
        ordering = ["sort_key"]

    def __str__(self):
        return str(self.id)


class PaymentTrans(CommonDateAndSafeDeleteMixin, TranslationModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(
        Payment, related_name="translations", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content_checkout = models.TextField(blank=True, null=True)
    content_checkout_result = models.TextField(blank=True, null=True)

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        db_table = settings.APP_NAME + "_payment_payment_trans"
        get_latest_by = "updated_at"
        index_together = (("language_code", "payment"),)
        ordering = ["language_code"]

    def __str__(self):
        return str(self.id)
