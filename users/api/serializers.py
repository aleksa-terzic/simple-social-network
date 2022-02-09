from rest_framework import serializers
from users.models import Profile, User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_profile(self, user):
        profile = Profile.objects.get(user=user)
        return ProfileSerializer(profile).data
