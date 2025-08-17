import re
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length)
        self.message = 'Password must be at least {} characters long.'.format(min_length)

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                self.message,
                code='password_too_short',
                params={'min_length': self.min_length},
            )

class ComplexPasswordValidator:
    """
    ตรวจสอบความซับซ้อนของรหัสผ่าน:
    - ความยาวอย่างน้อย 8 ตัว (เรายังคงมี MinimumLengthValidator ด้วย)
    - มีตัวพิมพ์ใหญ่ (A-Z)
    - มีตัวพิมพ์เล็ก (a-z)
    - มีตัวเลข (0-9)
    - มีอักขระพิเศษ (เช่น !@#$%)
    """
    def validate(self, password, user=None):
        if password is None:
            raise ValidationError(_('This password is invalid.'), code='password_no_value')

        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'), code='password_too_short')

        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'), code='password_no_upper')

        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'), code='password_no_lower')

        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one digit.'), code='password_no_digit')

        if not re.search(r'[^\w\s]', password):
            raise ValidationError(_('Password must contain at least one special character.'), code='password_no_special')

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, including at least one uppercase letter, "
            "one lowercase letter, one number and one special character."
        )
