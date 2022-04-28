from django.db import models


class Profile(models.Model):
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id_user} - {self.first_name} - {self.nickname}'

    class Meta:
        db_table = 'users'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['id_user']
