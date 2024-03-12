from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "username", "name", "birthday", "gender", "password"]


class UserMeSetializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["username", "name", "birthday", "gender", "email"]
