from api.views import BookReviewsViewSet
from rest_framework.routers import DefaultRouter
from api.views import UsersListAPIView, BookAuthorsListAPIView
# from api.views import BookReviewDetailAPIView, BookReviewsAPIView,
from django.urls import path

app_name = "api"


urlpatterns = [

    # path("reviews/", BookReviewsAPIView.as_view(), name="review-list"),
    # path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name="review-detail"),
    path("users/", UsersListAPIView.as_view(), name="users-list"),
    path("authors/", BookAuthorsListAPIView.as_view(), name="authors-list"),

]


# Linking urls in DRF ViewSet
router = DefaultRouter()
router.register('reviews', BookReviewsViewSet, basename='review')
urlpatterns += router.urls