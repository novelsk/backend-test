from rest_framework import permissions
from rest_framework.views import APIView


class LoginRequiredAPIView(APIView):
    """Basic view that handles user authorization at the DRF level.
    Use it like any other django class-based-view.
    """

    permission_classes = [permissions.IsAuthenticated]
