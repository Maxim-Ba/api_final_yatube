from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = SimpleRouter()
router_v1.register("posts", PostViewSet, basename="posts")
router_v1.register("groups", GroupViewSet, basename="groups")
router_v1.register("follow", FollowViewSet, basename="follow")
router_v1.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router_v1.urls)),
]
