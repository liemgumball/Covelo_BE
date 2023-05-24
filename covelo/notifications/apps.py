from django.apps import AppConfig
from rest_framework.response import Response
from exponent_server_sdk import PushMessage, PushClient

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

def send_notification(self, title, body, data, expo_push_token):
    message = PushMessage(title=title, body=body, data=data)
    client = PushClient()
    try:
        response = client.send_push_message_to_individual(
            message=message,
            recipient=expo_push_token
        )
        if response.is_success:
            print('Notification sent successfully')
        else:
            print('Notification failed to send:', response.errors)
    except Exception as e:
        print('Error sending notification:', str(e))

def send_notification_view(self):
    expo_push_token = "ExponentPushToken[QPiataO0qw6ZYNeVSxoHT2]"
    self.send_notification(
        "New message", "You have a new message", {}, expo_push_token)
    return Response("Notification sent")
