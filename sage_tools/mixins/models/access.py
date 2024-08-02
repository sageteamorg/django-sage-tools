# mixins.py
from django.core.exceptions import ValidationError

class SingletonModelMixin:
    def clean(self):
        model = self.__class__
        if model.objects.exists() and not self.pk:
            raise ValidationError(
                f'There is already a {model.__name__} entry. You can only update the existing one.'
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super(SingletonModelMixin, self).save(*args, **kwargs)
