from django.db.models import Model, ForeignKey, BooleanField, DateTimeField, DO_NOTHING
from django.utils.translation import gettext_lazy as _


class CoreModel(Model):
    is_active = BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )

    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At'),
        null=True, blank=True
    )

    created_by = ForeignKey(
        'auth.User',
        null=True, blank=True,
        on_delete=DO_NOTHING,
        related_name='%(app_label)s_%(class)s_created_by'
    )

    updated_at = DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At'),
        null=True, blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk}"
