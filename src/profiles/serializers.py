from rest_framework import serializers
from .models import SecureUser, Invite


class CreateSecureUserSerializer(serializers.ModelSerializer):
    """ Output info about the user
    """

    class Meta:
        model = SecureUser
        exclude = (
            'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'safe_user', 'last_login',
            'date_joined'
        )


class GetShorUserInfoSerializer(serializers.ModelSerializer):
    """ Get Short info about User
    """
    class Meta:
        model = SecureUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email',
        )


class GetPublicSecureUserSerializer(serializers.ModelSerializer):
    """ Output of public info about the user
    """

    class Meta:
        model = SecureUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'phone', 'date_of_birth', 'gender',
            'city', 'bio', 'safe_user', 'is_active', 'is_superuser'
        )


class GetDetailSecureUserSerializer(GetPublicSecureUserSerializer):
    """ Detail user serializer
    """
    safe_user = GetShorUserInfoSerializer(many=True)


class GetPublicMessageUserSerializer(serializers.ModelSerializer):
    """ Output of public info about the user to use in message
    """

    class Meta:
        model = SecureUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email'
        )


class GetUserForInvite(serializers.ModelSerializer):
    """ Output of public info about the user in invite view
    """

    class Meta:
        model = SecureUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'phone', 'date_of_birth', 'gender',
        )


class ListSendInviteSerializer(serializers.ModelSerializer):
    """ Get List invite to other users
    """
    to_user = GetUserForInvite(read_only=True)

    class Meta:
        model = Invite
        fields = ('id', 'to_user',)


class ListReceiveInviteSerializer(serializers.ModelSerializer):
    """ Get List invite from other users
    """
    from_user = GetUserForInvite(read_only=True)

    class Meta:
        model = Invite
        fields = ('id', 'from_user',)
