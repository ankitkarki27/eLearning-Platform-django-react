from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import CustomPermission
from rest_framework.permissions import IsAdminUser
from users.serializers import UserAccountSerializer
from rest_framework import status
from users.models import UserAccount
from django.db.models import Sum
# from users.models

class UserAccountViewSet(ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = []
        elif self.action == "list":
            self.permission_classes = [IsAdminUser]
        elif self.action in ["retrieve", "update", "destroy"]:
            self.permission_classes = [CustomPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.is_superuser or request.user == user:
            return super().retrieve(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden"})

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_superuser:
            if "is_staff" in request.data or "is_superuser" in request.data:
                raise PermissionDenied(
                    "You do not have permission to modify these fields."
                )
        if request.user.is_superuser or request.user == user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden"})

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.is_superuser or request.user == user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Forbidden"})

    @action(detail=False, methods=["GET"])
    # ! Returns a user by email if exists
    def get_user_by_email(self, request):
        email = request.query_params.get("email")
        user = UserAccount.objects.filter(email=email).first()
        if user:
            return Response(UserAccountSerializer(user).data)
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"detail": "User not found"}
        )

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    # ! Returns the current logged-in user's info
    def get_user(self, request):
        return Response(UserAccountSerializer(request.user).data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAdminUser])
    # Admin-only(Returns all students)
    def get_students(self, request):
        students = UserAccount.objects.filter(role="student")
        return Response(UserAccountSerializer(students, many=True).data)

    
    @action(detail=False, methods=["GET"], permission_classes=[IsAdminUser])
    # get admins
    # returns all users with role admin
    
    def get_admins(self,request):
        admins = UserAccount.objects.filter(role="admin")
        return Response(UserAccountSerializer(admins, many=True).data)
    
   
    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def update_contact_info(self, request):
        user = request.user
        data = request.data

        full_name = data.get("full_name")
        profile_image = data.get("profile_image")
        phone_number = data.get("phone_number")

        if full_name:
            user.full_name = full_name
        if profile_image:
            user.profile_image = profile_image
        if phone_number:
            user.phone_number = phone_number

        user.save()
        return Response(UserAccountSerializer(user).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    # ! Get all users by role (e.g., ?role=student)
    def get_users_by_role(self, request):
        role = request.query_params.get("role")
        if role:
            users = UserAccount.objects.filter(role=role)
            return Response(UserAccountSerializer(users, many=True).data)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"detail": "Role parameter is required"}
        )
