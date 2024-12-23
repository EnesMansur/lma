from django.contrib.auth.models import User

from rest_framework import serializers

from membership.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        profile = Profile.objects.create(
            user=user,
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(
                instance=instance.user,
                data=user_data,
                partial=True
            )

            user_serializer.is_valid(
                raise_exception=True
            )

            user_serializer.save()

        # Update Profile
        return super().update(instance, validated_data)
