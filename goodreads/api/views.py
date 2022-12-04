from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from books.models import BookReview
from api.serializers import BookReviewSerializer, LoggedUsersListSerializer, AuthorsListSerializer
from users.models import CustomUser
from rest_framework.response import Response
from rest_framework.views import APIView
from books.models import Author
from rest_framework import generics
from rest_framework import viewsets



class UsersListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoggedUsersListSerializer
    queryset = CustomUser.objects.all().order_by('id')



class BookAuthorsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorsListSerializer
    queryset = Author.objects.all()



# DRF ViewSet to provides you to reduce your views and collect them one view
class BookReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    lookup_field = 'id'



# class BookReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all()
#     lookup_field = 'id'
#
#
    # def get(self, request, id):
    #     book_review = BookReview.objects.get(id=id)
    #     serializer = BookReviewSerializer(book_review)
    #     return Response(data=serializer.data)
#     #
#     #
#     #
#     # def delete(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     book_review.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
#     #
#     #
#     #
#     # def put(self, request, id):
#     #     book_review = BookReview.objects.get(id=id)
#     #     serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
#     #
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(status=status.HTTP_200_OK)
#     #
#     #     return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#     #
#     #
#     #
#
#
# class BookReviewsAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         book_reviews = BookReview.objects.all()
#         paginator = PageNumberPagination()
#         page_obj = paginator.paginate_queryset(book_reviews, request)
#         serializer = BookReviewSerializer(page_obj, many=True)
#
#         return paginator.get_paginated_response(serializer.data)
#
#
#
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#
#




