from django.urls import include, path
from rest_framework.routers import DefaultRouter
from workout import views

router = DefaultRouter()
router.register("tags", views.TagViewSet)
router.register("exercises", views.ExerciseViewSet)

app_name = "workout"

urlpatterns = [path("", include(router.urls))]
