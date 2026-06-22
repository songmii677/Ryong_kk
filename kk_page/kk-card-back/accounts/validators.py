import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    def validate(self, password, user=None):
        has_letter = re.search(r'[A-Za-z]', password)
        has_number = re.search(r'[0-9]', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\\[\]~`]', password)

        if not has_letter or not has_number or not has_special:
            raise ValidationError(
                _('비밀번호는 영문, 숫자, 특수문자를 모두 포함해야 합니다.'),
                code='password_not_complex',
            )

    def get_help_text(self):
        return _('비밀번호는 영문, 숫자, 특수문자를 모두 포함해야 합니다.')