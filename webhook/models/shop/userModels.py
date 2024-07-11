from django.db import models

class Role(models.TextChoices):
    DEFAULT = 'DEFAULT', 'Default'
    COURIER = 'COURIER', 'Courirer'
    MANAGER = 'MANAGER', 'Manager'
    ADMIN = 'ADMIN', 'Admin'

ROLE_LEVELS = {
    Role.DEFAULT: 0,
    Role.COURIER: 1,
    Role.MANAGER: 2,
    Role.ADMIN: 3,
}