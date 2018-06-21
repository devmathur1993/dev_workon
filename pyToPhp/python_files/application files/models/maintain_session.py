from django.db import models

class MaintainSession(models.Model):
    pk_session_key = models.BigAutoField(db_column='PK_session_key', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=100)
    useremail = models.CharField(max_length=100)
    session_time = models.TimeField(blank=True, null=True)
    link_used = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maintain_session'

