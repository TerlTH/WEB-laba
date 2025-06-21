from rest_framework import serializers
from .models import Note
from .models import Product

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # Только для чтения, имя владельца
    class Meta:
        model = Note
        fields = '__all__'
        extra_kwargs = {
            'file': {'required': False, 'allow_null': True} # Поле file не обязательно
        }

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # Только для чтения, имя владельца

    class Meta:
        model = Product
        fields = '__all__' # Включить все поля модели