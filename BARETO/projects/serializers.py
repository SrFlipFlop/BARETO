from rest_framework import serializers

from models import Project, Asset, Vulnerability

class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=250)
    status = serializers.CharField(required=False, allow_blank=True, max_length=250)
    start = serializers.DateTimeField(required=False, allow_blank=True)
    finished = serializers.DateTimeField(required=False, allow_blank=True)
    notes = serializers.TextField()

    def create(self, data):
        return Snippet.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.status = data.get('status', instance.status)
        instance.start = data.get('start', instance.start)
        instance.finished = data.get('finished', instance.finished)
        instance.notes = data.get('notes', instance.notes)
        instance.save()
        return instance