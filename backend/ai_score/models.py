from django.db import models


class FitScore(models.Model):
    CONTENT_TYPES = [
        ('bootcamp', '부트캠프'),
        ('job', '채용공고'),
        ('certification', '자격증'),
        ('competition', '공모전'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='fit_scores',
    )
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    score = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        indexes = [
            models.Index(fields=['user', 'content_type', 'score']),
        ]
