from django.contrib.auth import get_user_model
from django.db.models.fields import SlugField
from rest_framework import serializers
from newsletter.models import Newsletter, Subscription
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = [
            "ip", "activation_code", "subscribed", "subscribe_date", "user",
            "unsubscribed", "unsubscribe_date", "name_field", "newsletter"
        ]

    def create(self, validated_data):
        
        email = validated_data.get("email_field")
        newsletter = Newsletter.objects.get(slug="feline")
        subscriber = Subscription.objects.create(
            name_field = email,
            email_field = email,
            newsletter = newsletter,
            subscribed=True
        ) 

        subscriber.send_activation_email("subscribe")

        return subscriber