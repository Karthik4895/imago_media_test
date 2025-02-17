from rest_framework import serializers

class MediaSerializer(serializers.Serializer):
    bildnummer = serializers.CharField()
    datum = serializers.DateTimeField()
    suchtext = serializers.CharField()
    fotografen = serializers.CharField(allow_null=True, required=False)
    hoehe = serializers.IntegerField()
    breite = serializers.IntegerField()
    db = serializers.CharField()
