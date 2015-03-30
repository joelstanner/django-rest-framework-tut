from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html'
    )

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner', 'id', 'title', 'code',
                  'line_nums', 'language', 'style')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the
        validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.line_nums = validated_data.get('line_nums', instance.line_nums)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet=detail', read_only=True
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'snippets')
