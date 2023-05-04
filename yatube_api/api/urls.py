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
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
    path("", include(router_v1.urls)),
]
