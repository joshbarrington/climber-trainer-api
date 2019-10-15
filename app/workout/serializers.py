from rest_framework import serializers

from core.models import Tag, Exercise


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag ojects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for exercise object"""

    class Meta:
        model = Exercise
        fields = ('id', 'name')
        read_only_fields = ('id', )
