from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    #email = request.data.get('email', '')
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username','email', 'password', 'team_id')

    # def create(self, validated_data):
    #     print("UserRegistrationSerializer create:",validated_data)
    #     data_email = validated_data.pop('email')
    #     data_username=data_email.split('@')[0]
    #     #try:
    #     user = User.objects.create(**validated_data, username=data_username)
    #     #except IntegrityError:
    #     #    return Response({}, status=status.HTTP_400_BAD_REQUEST)
    #     return user