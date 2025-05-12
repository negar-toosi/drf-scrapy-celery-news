from django.db import models
from django.db.models import Q
from django.core.validators import MaxLengthValidator
from technews.common.models import BaseModel

class Tags(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        db_table_comment = "Stores tags used to label news articles."

class News(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    summary = models.TextField(
        validators=[MaxLengthValidator(500)],
        blank=True) # Short summary or excerpt for preview
    source = models.URLField(max_length=256) 
    tags = models.ManyToManyField( 
        Tags, 
        related_name='news' # Allows reverse access
        )
    published_at = models.DateTimeField(null=True, blank=True) 
    status = models.BooleanField(default=False) # Publication status: True = Published, False = Draft

    class Meta:
        db_table_comment = "Table for storing news posts"
        ordering = ['-created_at']
        constraints = [
            # Ensures that the same news title can't be added more than once from the same source
            models.UniqueConstraint(
                fields = ["title","source"], 
                name = 'unique_news_per_source'),
            
            # Ensures that a news article marked as published (status=True) must have a published date
            models.CheckConstraint(
                check = Q(status=True) & Q(published_at__isnull=False),
                name = "published_news_must_have_date"
            ),
        ]

    def __str__(self):
        return self.title
