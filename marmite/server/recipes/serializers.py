from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, Unit


class IngredientSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=1000)
    plural_name = serializers.CharField(max_length=1000)
    type = serializers.CharField(max_length=1000)
    tags = serializers.JSONField()
    allergies = serializers.JSONField()
    created_at = serializers.DateTimeField(read_only=True)
    last_updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RecipeSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=1000)
    short_description = serializers.CharField()
    type = serializers.CharField(max_length=1000)
    source = serializers.CharField(max_length=1000)
    preparation_time = serializers.IntegerField()
    cooking_time = serializers.IntegerField()
    instructions = serializers.CharField()
    image = serializers.URLField()
    created_at = serializers.DateTimeField(read_only=True)
    last_updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):

    ingredients = IngredientSerializer(many=True, read_only=True)


class UnitSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=1000)
    plural_name = serializers.CharField(max_length=1000)
    symbol = serializers.CharField(max_length=5)
    unit_system = serializers.CharField(max_length=1000)
    created_at = serializers.DateTimeField(read_only=True)
    last_updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Unit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)
    quantity = serializers.IntegerField()
    unit = UnitSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    last_updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return RecipeIngredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
