from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["book", "reviewer", "review_text", "rating"]
