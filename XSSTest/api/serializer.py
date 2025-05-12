from rest_framework.serializers import ModelSerializer
from .models import Comment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            fio=validated_data["fio"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
