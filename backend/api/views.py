from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile

@api_view(['GET'])
def get_users(request):
    users = UserProfile.objects.all().values('id', 'username', 'email')
    return Response(users)