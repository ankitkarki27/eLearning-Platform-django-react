from django.shortcuts import render
from users.models import UserAccount
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from users.permissions import *
from main.models import *
from main.serializers import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from django.db.models import Sum
# from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    # permission_classes=[IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Duplicate category name"}
               )
            
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Duplicate category name"}
               )
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Category cannot be deleted"}
               )
    
    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            kwargs["many"] = True
            return CategoryListSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)
    
    

# course viewset
    
class CourseViewSet(ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializer
    permission_classes=[CustomPermission]
    search_fields=["title"]
    filterset_fields=["category"]
    lookup_field="slug"
    filter_backends = [filters.SearchFilter]    # Allows searching by title
    
    # filter_backends = [DjangoFilterBackend]  # Allows filtering by category
    # filterset_fields = ['category']  # Specify the filter fields
    
    def create(self, request, *args, **kwargs):
        try:
          #only instructor can create course
          if not request.user.role=="instructor":
              return Response(
                  status=status.HTTP_403_FORBIDDEN,
                  data={"detail":"You are not instructor so your arenot allowed to create course"}
              )
              return super().create(request, *args, **kwargs)
        except Exception as e:
              return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Duplicate course title"}
               )
    
    def update(self, request, *args, **kwargs):
        if request.data.get("is_published") == False:
            course=Course.objects.get(slug=kwargs["slug"])
            # Check if there are any enrollments for the course
            if Enrollment.objects.filter(course=course).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"detail":"Course cannot be unpublished as it has enrolled students"}
                )
            
        return super().update(request, *args, **kwargs)
          
    def destroy(self, request, *args, **kwargs):
        
        Course=self.get_object()
        # Check if there are any enrollments for the course
        if Enrollment.objects.filter(course=Course).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail":"Course cannot be deleted as it has enrolled students"}
            )
        return super().destroy(request, *args, **kwargs)


    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_published_courses(self, request):
        queryset = self.get_queryset().filter(is_published=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def get_my_courses(self, request):
        if request.user.role == "student":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail":"You are not allowed to access this endpoint"}
            )
        courses=Course.objects.filter(instructor=request.user)
        serializer=self.get_serializer(courses,many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def get_all_course(self,request,slug=None):
        course=self.get_object()
        serializer=self.get_serializer(course)
        return Response(serializer.data)
    
    
    # net to review again from here to below
    @action(detail=False, methods=["GET"])
    def get_stats(self, request):
        if request.user.role != "instructor":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail": "Forbidden"}
            )
        courses_count = Course.objects.filter(instructor=request.user).count()
        published_count = Course.objects.filter(instructor=request.user, is_published=True).count()
        student_count = Enrollment.objects.filter(course__instructor=request.user).exclude(user=request.user).count()
        total_earning = Payment.objects.filter(course__instructor=request.user).aggregate(total=Sum("amount"))

        return Response({
            "courses": courses_count,
            "published_courses": published_count,
            "students": student_count,
            "income": total_earning["total"] or 0.0
        })

    @action(detail=False, methods=["GET"])
    def get_student_count(self, request):
        course_id = request.query_params.get("course_id")
        if not course_id:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"detail": "course_id required in query parameter."}
            )
        try:
            course = Course.objects.get(id=course_id)
            count = Enrollment.objects.filter(course=course).exclude(user=course.instructor).count()
            return Response({"student_count": count})
        except Course.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Course not found."}
            )
    
