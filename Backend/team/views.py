from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import TeamMember
from .serializers import TeamMemberSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins/staff to edit.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS allowed to anyone
        return request.user and request.user.is_staff


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.select_related('user').all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
