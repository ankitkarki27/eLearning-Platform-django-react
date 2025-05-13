from django.shortcuts import render
from users.models import UserAccount
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from users.permissions import *
from main.models import *
from main.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from django.db.models import Sum
from django.db import IntegrityError
# from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

#custom permission class
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow only cretain users of admin role
        if view.action in ["create", "update", "destroy"]:
            return request.user.role == "admin"
        return True
       

#category viewset
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
    filterset_fields=["category","is_published","admin"]
    lookup_field="slug"
    filter_backends = [filters.SearchFilter]    # Allows searching by title
    
    # filter_backends = [DjangoFilterBackend]  # Allows filtering by category
    # filterset_fields = ['category']  # Specify the filter fields
    
    def create(self, request, *args, **kwargs):
        try:
          #check if user is admin
          if not request.user.role=="admin":
              return Response(
                  status=status.HTTP_403_FORBIDDEN,
                  data={"detail":"Only admin can create course"}
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
        courses=Course.objects.filter(admin=request.user)
        serializer=self.get_serializer(courses,many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def get_all_course(self,request,slug=None):
        course=self.get_object()
        serializer=self.get_serializer(course)
        return Response(serializer.data)
    
    # get course by category
    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def get_stats(self, request):
        if request.user.role != "admin":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"detail": "Forbidden"}
            )
        #fetching stats for admin
        courses_count = Course.objects.filter(admin=request.user).count()
        published_count = Course.objects.filter(admin=request.user, is_published=True).count()
        student_count = Enrollment.objects.filter(course__admin=request.user).exclude(user=request.user).count()
        
        # total earnins
        total_earning = Payment.objects.filter(course__admin=request.user).aggregate(total=Sum("amount"))
        total_income= total_earning["total"] if total_earning["total"] else 0.0
        
        return Response({
            "courses": courses_count,
            "published_courses": published_count,
            "students": student_count,
            "total_income": total_income
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
            count = Enrollment.objects.filter(course=course).exclude(user=course.admin).count()
            return Response({"student_count": count})
        except Course.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Course not found."}
            )
    

# section viewset
class SectionViewSet(ModelViewSet):
    queryset=Section.objects.all()
    serializer_class=SectionSerializer
    permission_classes=[CustomPermission]
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Duplicate section title"}
               )
            
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Duplicate section title"}
               )
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_409_CONFLICT,data={"detail":"Section cannot be deleted"}
               )

#cart viewset
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all().select_related("course", "student")
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Students see only their cart, admins see all
        if self.request.user.role == 'student':
            return self.queryset.filter(student=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"detail": "course_id required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response(
                {"detail": "Already enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Cart.objects.filter(student=request.user, course=course).exists():
            return Response(
                {"detail": "Course already in cart"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={
            'course': course.id,
            'student': request.user.id
        })
        
        serializer.is_valid(raise_exception=True)
        serializer.save()  #creates the cart record in DB
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["DELETE"])
    def clear_cart(self, request):
        #clear the cart for the logged-in student
        self.get_queryset().filter(student=request.user).delete()
        return Response(
            {"detail": "Cart cleared successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["GET"])
    def cart_total(self, request):
        # Calculate the total price of items in the cart.
        cart_items = self.get_queryset().filter(student=request.user)
        total = sum(item.course.price for item in cart_items)
        return Response({
            "total": total,
            "item_count": cart_items.count()
        })

#enrollment viewset

#payment viewset

#attachment viewset
class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all().select_related('section')
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]  # Default permission

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]  # Changed from IsAdminUser
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [CustomPermission]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            # Validate section exists and user has permission
            section_id = request.data.get('section')
            if not section_id:
                return Response(
                    {"detail": "section field is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Additional validation can be added here
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "Duplicate entry or invalid data"},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
#certificate viewset //will be done later

