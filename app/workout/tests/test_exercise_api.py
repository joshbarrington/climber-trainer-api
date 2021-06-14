from core.models import Exercise
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from workout.serializers import ExerciseSerializer

EXERCISE_URL = reverse("workout:exercise-list")


class PublicExerciseApiTest(TestCase):
    """Test the publicly available exercise API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required for endpoint access"""
        res = self.client.get(EXERCISE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExerciseApiTest(TestCase):
    """Test prviate exercises API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@email.com", "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_exercise_list(self):
        """Test retrieving list of exercises"""
        Exercise.objects.create(user=self.user, name="Pull Up")
        Exercise.objects.create(user=self.user, name="Push Up")

        res = self.client.get(EXERCISE_URL)

        exercises = Exercise.objects.all().order_by("-name")
        serializer = ExerciseSerializer(exercises, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_exercise_list_limited_to_user(self):
        """Test exercises for authenticated user are returned"""

        user2 = get_user_model().objects.create_user("test2@email.com", "testpassword")
        Exercise.objects.create(user=user2, name="Weighted Pull Ups")
        exercise = Exercise.objects.create(user=self.user, name="Pull Up Negatives")

        res = self.client.get(EXERCISE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], exercise.name)

    def test_create_exercise_successful(self):
        """Test create new exercise"""
        payload = {"name": "Plank"}
        self.client.post(EXERCISE_URL, payload)

        exists = Exercise.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)

    def test_create_exercise_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {"name": ""}
        res = self.client.post(EXERCISE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
