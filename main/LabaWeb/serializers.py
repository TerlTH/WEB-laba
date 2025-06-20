from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Note
        fields = '__all__'
        extra_kwargs = {
            'file': {'required': False, 'allow_null': True}
        }