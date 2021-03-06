from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Specialty, Badge, UserSpecialty
from .serializers import SpecialtySerializer, UserSpecialtySerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .tasks import take_screenshot

@api_view(['GET'])
@permission_classes([AllowAny])
def get_specialties(request):
    items = Specialty.objects.all()
    serializer = SpecialtySerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_badges(request):
    items = Badge.objects.all()
    serializer = SpecialtySerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_certificate(request, token):
    item = UserSpecialty.objects.filter(token=token).first()
    if item is None:
        raise NotFound('Certificate not found')

    serializer = UserSpecialtySerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

@receiver(post_save, sender=UserSpecialty)
def post_save_course_dosomething(sender,instance, **kwargs):
    if instance.preview_url is None or instance.preview_url == "":
        take_screenshot.delay(instance.id)

# @api_view(['GET'])
# def get_single_course(request, course_slug):
#     course = Course.objects.filter(slug=course_slug).first()
#     if course is None:
#         raise serializers.ValidationError("Course slug not found", code=404)
#     serializer = GetCourseSerializer(course, many=False)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# class SyllabusView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, course_slug=None, version=None):
#         course = Course.objects.filter(slug=course_slug).first()
#         if course is None:
#             raise serializers.ValidationError("Course slug not found", code=404)

#         syl = None
#         if version is None:
#             syl = course.syllabus_set.all()
#             serializer = SyllabusSmallSerializer(syl, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             syl = course.syllabus_set.filter(version=version).first()
        
#         if syl is None:
#             raise serializers.ValidationError("Syllabus not found", code=404)

#         serializer = SyllabusGetSerializer(syl, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self, request, course_slug=None):
#         version = 1
#         course = Course.objects.filter(slug=course_slug).first()
#         if course is None:
#             raise serializers.ValidationError(f"Invalid course slug {course__slug}", code=404)

#         item = Syllabus.objects.filter(course__slug=course_slug).order_by('version').first()

#         if item is not None:
#             version = item.version + 1

#         serializer = SyllabusSerializer(data=request.data, context={"course": course})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, course_slug=None, version=None):
#         if version is None:
#             raise serializers.ValidationError("Missing syllabus version", code=400)
        
#         item = Syllabus.objects.filter(course__slug=course_slug, version=version).first()
#         if item is None:
#             raise serializers.ValidationError("Syllabus version not found", code=404)
        
#         serializer = SyllabusSerializer(item, data=request.data, many=False)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
