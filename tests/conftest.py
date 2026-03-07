import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def api_client():
    """Фикстура для тестового API-клиента DRF."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фабрика для создания курсов через model_bakery."""
    def create_course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return create_course


@pytest.fixture
def student_factory():
    """Фабрика для создания студентов через model_bakery."""
    def create_student(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return create_student
