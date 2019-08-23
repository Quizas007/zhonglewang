from django.core.exceptions import ValidationError

def valid_mode(n):
    if n < 1 or n > 2:
        raise ValidationError("模式不存在！")