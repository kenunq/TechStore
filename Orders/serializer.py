from rest_framework import serializers

from Orders.models import Order, UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user_info = UserInfoSerializer()

    class Meta:
        model = Order
        exclude = ["user"]
