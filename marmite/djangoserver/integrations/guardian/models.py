from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework import serializers


class RecipeGuardian(models.Model):

    class Meta:
        db_table = 'recipes_guardian'

    id = models.CharField(max_length=1000, primary_key=True)
    section_id = models.CharField(max_length=255)
    section_name = models.CharField(max_length=255)
    web_publication_date = models.DateTimeField()
    web_title = models.CharField(max_length=1000)
    web_url = models.CharField(max_length=1000)
    api_url = models.CharField(max_length=1000)
    trail_text = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    standfirst = models.TextField()
    body = models.TextField()
    main = models.TextField()
    production_office = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    lang = models.CharField(max_length=255)
    body_text = models.TextField()
    last_modified = models.DateTimeField()
    short_url = models.CharField(max_length=1000)
    thumbnail = models.CharField(max_length=1000)
    wordcount = models.BigIntegerField()
    byline = models.CharField(max_length=1000)
    star_rating = models.BigIntegerField()
    tags = JSONField()
    pillar_name = models.CharField(max_length=255)
    pillar_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class RecipeGuardianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeGuardian
        fields = ('id', 'section_id', 'section_name', 'web_publication_date', 'web_title', 'web_url', 'api_url', 'trail_text', 'headline', 'standfirst', 'body', 'main', 'production_office', 'publication', 'lang', 'body_text', 'last_modified', 'short_url', 'thumbnail', 'wordcount', 'byline', 'star_rating', 'tags', 'pillar_name', 'pillar_id', 'created_at', 'last_updated_at')