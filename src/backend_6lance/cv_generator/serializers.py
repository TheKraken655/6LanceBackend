from rest_framework import serializers

class CvUserDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    surname = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=200)
    cuil = serializers.CharField(max_length=200)
    postal_code = serializers.IntegerField()
    address = serializers.CharField(max_length=200)
    province = serializers.CharField(max_length=200)
    birth_date = serializers.DateField()
    dni = serializers.IntegerField()