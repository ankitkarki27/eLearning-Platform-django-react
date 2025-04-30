from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import CustomPermission
from rest_framework.permissions import IsAdminUser
from users.serializers import UserSerializer
from rest_framework import status
from users.models import User
from django.db.models import Sum
# from users.models

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
        user = User.objects.filter(email=email).first()
        if user:
            return Response(UserSerializer(user).data)
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"detail": "User not found"}
        )

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    # ! Returns the current logged-in user's info
    def get_user(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAdminUser])
    # Admin-only(Returns all students)
    def get_students(self, request):
        students = User.objects.filter(role="student")
        return Response(UserSerializer(students, many=True).data)

    @action(detail=False, methods=["POST"], permission_classes=[IsAdminUser])
    # Admin-only: Approves instructor by setting is_verified to True
    def approve_instructor(self, request):
        user_id = request.data.get("user_id")
        user = User.objects.filter(id=user_id).first()
        if user:
            user.is_verified = True
            user.save()
            return Response(UserSerializer(user).data)
        return Response(
            status=status.HTTP_404_NOT_FOUND, data={"detail": "User not found"}
        )

    @action(detail=False, methods=["GET"], permission_classes=[IsAdminUser])
    # Admin-only: Returns instructors with total earnings sorted
    def get_instructors(self, request):
        from main.models import Payment

        instructors = User.objects.filter(role="instructor")
        for instructor in instructors:
            total_earning = Payment.objects.filter(
                course__instructor=instructor
            ).aggregate(total_earning=Sum("amount"))["total_earning"]
            instructor.total_earning = total_earning if total_earning else 0
        instructors = sorted(instructors, key=lambda x: x.total_earning, reverse=True)
        return Response(UserSerializer(instructors, many=True).data)

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
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    # ! Get all users by role (e.g., ?role=student)
    def get_users_by_role(self, request):
        role = request.query_params.get("role")
        if role:
            users = User.objects.filter(role=role)
            return Response(UserSerializer(users, many=True).data)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, data={"detail": "Role parameter is required"}
        )
