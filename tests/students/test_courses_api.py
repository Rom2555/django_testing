import pytest
from django.urls import reverse

from students.models import Course


@pytest.mark.django_db
class TestCourseRetrieveAPI:
    """Тесты для получения одного курса (retrieve-логика)"""

    def test_retrieve_single_course(self, api_client, course_factory):
        """Проверка получения одного курса по id"""
        # Создаем курс через фабрику
        course = course_factory(name="Test Course")

        # Строим URL и делаем запрос
        url = reverse("courses-detail", kwargs={"pk": course.id})
        response = api_client.get(url)

        # Проверяем, что вернулся курс, который запрашивали
        assert response.status_code == 200
        assert response.data["id"] == course.id
        assert response.data["name"] == course.name


@pytest.mark.django_db
class TestCourseListAPI:
    """Тесты для получения списка курсов (list-логика)"""

    def test_list_courses(self, api_client, course_factory):
        """Проверка получения списка курсов"""
        # Создаем несколько курсов через фабрику
        course1 = course_factory(name="Course 1")
        course2 = course_factory(name="Course 2")
        course3 = course_factory(name="Course 3")

        # Делаем запрос списка курсов
        url = reverse("courses-list")
        response = api_client.get(url)

        # Проверяем результат
        assert response.status_code == 200
        assert len(response.data) == 3

        # Проверяем, что все созданные курсы присутствуют в ответе
        course_ids = [item["id"] for item in response.data]
        assert course1.id in course_ids
        assert course2.id in course_ids
        assert course3.id in course_ids


@pytest.mark.django_db
class TestCourseFilterAPI:
    """Тесты для фильтрации списка курсов"""

    def test_filter_courses_by_id(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по id."""
        # Создаем курсы через фабрику
        course1 = course_factory(name="Course 1")
        course2 = course_factory(name="Course 2")
        course3 = course_factory(name="Course 3")

        # Делаем запрос с фильтром по id одного курса
        url = reverse("courses-list")
        response = api_client.get(url, {"id": course2.id})

        # Проверяем результат
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == course2.id

    def test_filter_courses_by_name(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по name"""
        # Создаем курсы через фабрику
        course1 = course_factory(name="Python")
        course2 = course_factory(name="Basic")
        course3 = course_factory(name="Assembler")

        # Делаем запрос с фильтром по name
        url = reverse("courses-list")
        response = api_client.get(url, {"name": "Python"})

        # Проверяем результат
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Python"


@pytest.mark.django_db
class TestCourseCreateAPI:
    """Тесты для создания курса"""

    def test_create_course_success(self, api_client):
        """Проверка успешного создания курса"""
        # JSON-данные для создания курса
        data = {
            "name": "New Course",
        }

        # Делаем POST-запрос на создание
        url = reverse("courses-list")
        response = api_client.post(url, data, format="json")

        # Проверяем результат
        assert response.status_code == 201
        assert response.data["name"] == data["name"]
        assert "id" in response.data

        # Проверяем, что курс создан в БД
        course = Course.objects.get(id=response.data["id"])
        assert course.name == data["name"]


@pytest.mark.django_db
class TestCourseUpdateAPI:
    """Тесты для обновления курса"""

    def test_update_course_success(self, api_client, course_factory):
        """Проверка успешного обновления курса"""
        # Создаем курс через фабрику
        course = course_factory(name="Test Name")

        # JSON-данные для обновления
        data = {
            "name": "Updated Name",
        }

        # Делаем PUT-запрос на обновление
        url = reverse("courses-detail", kwargs={"pk": course.id})
        response = api_client.put(url, data, format="json")

        # Проверяем результат
        assert response.status_code == 200
        assert response.data["name"] == data["name"]

        # Проверяем, что курс обновлен в БД
        course.refresh_from_db()
        assert course.name == data["name"]


@pytest.mark.django_db
class TestCourseDeleteAPI:
    """Тесты для удаления курса"""

    def test_delete_course_success(self, api_client, course_factory):
        """Проверка успешного удаления курса"""
        # Создаем курс через фабрику
        course = course_factory(name="Course to Delete")
        course_id = course.id

        # Делаем DELETE-запрос
        url = reverse("courses-detail", kwargs={"pk": course_id})
        response = api_client.delete(url)

        # Проверяем результат
        assert response.status_code == 204

        # Проверяем, что курс удален из БД
        assert not Course.objects.filter(id=course_id).exists()
