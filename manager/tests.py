from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import User
from .models import EventCategory, Event, Note, Task


class EventCategoryTestCase(APITestCase):

    def setUp(self):

        user_data = {
            "username": "MarikLNU_matema",
            "first_name": "Maria",
            "last_name": "Maria1",
            "email": "matema.group@gmail.com",
            "password": "OLGGG1234olggg!!!***1234",
            "re_password": "OLGGG1234olggg!!!***1234"
        }
        response = self.client.post('/auth/users/', user_data, format='json')  # Додайте format='json'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        # Отримання JWT токенів
        response = self.client.post('/auth/jwt/create/', {
            "username": "MarikLNU_matema",
            "password": "OLGGG1234olggg!!!***1234"
        }, format='json')  # Додайте format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.category1 = EventCategory.objects.create(name="Category1", description="Description1")
        self.category2 = EventCategory.objects.create(name="Category2", description="Description2")

    def test_get_all_eventcategories(self):
        response = self.client.get('/event-categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_eventcategory(self):
        response = self.client.get(f'/event-categories/{self.category1.id}/')  # Використання динамічного ID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Category1')

    def test_post_eventcategory(self):
        data = {"name": "Category3", "description": "Description3"}
        response = self.client.post('/event-categories/', data, format='json')  # Додавання format='json'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_eventcategory(self):
        data = {"name": "UpdatedCategory"}
        response = self.client.patch(f'/event-categories/{self.category1.id}/', data, format='json')  # Додавання format='json'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UpdatedCategory')

    def test_delete_eventcategory(self):
        response = self.client.delete('/event-categories/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EventTestCase(APITestCase):

    def setUp(self):
        # Створення тестового користувача
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "re_password": "testpassword123"
        }
        self.client.post('/auth/users/', self.user_data, format='json')

        # Отримання JWT токенів
        response = self.client.post('/auth/jwt/create/', {
            "username": "testuser",
            "password": "testpassword123"
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Створення категорії подій і нотаток
        self.category = EventCategory.objects.create(name="TestCategory", description="TestDescription")
        self.note1 = Note.objects.create(name="Note1", description="Description1")
        self.note2 = Note.objects.create(name="Note2", description="Description2")

        # Створення події
        self.event = Event.objects.create(
            name="TestEvent",
            description="EventDescription",
            is_public=True,
            created_by=User.objects.get(username="testuser"),
            category=self.category
        )
        self.event.notes.set([self.note1, self.note2])
        self.event.attendees.set([User.objects.get(username="testuser")])

    def test_get_all_events(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_event(self):
        response = self.client.get(reverse('event-detail', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'TestEvent')

    def test_update_event(self):
        data = {"name": "UpdatedEvent", "description": "UpdatedDescription"}
        response = self.client.patch(reverse('event-detail', kwargs={'pk': self.event.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=self.event.id).name, 'UpdatedEvent')

    def test_delete_event(self):
        response = self.client.delete(reverse('event-detail', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)


class NoteTestCase(APITestCase):

    def setUp(self):
        # Створення тестового користувача та отримання JWT токена
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword123")
        response = self.client.post('/auth/jwt/create/', {
            "username": "testuser",
            "password": "testpassword123"
        }, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Створення тестових нотаток
        self.note1 = Note.objects.create(name="Note1", description="Description1")
        self.note2 = Note.objects.create(name="Note2", description="Description2")

    def test_create_note(self):
        data = {"name": "Note3", "description": "Description3"}
        response = self.client.post(reverse('note-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 3)
        self.assertEqual(Note.objects.get(name="Note3").description, "Description3")

    def test_get_all_notes(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_note(self):
        response = self.client.get(reverse('note-detail', kwargs={'pk': self.note1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Note1')

    def test_update_note(self):
        data = {"name": "UpdatedNote", "description": "UpdatedDescription"}
        response = self.client.patch(reverse('note-detail', kwargs={'pk': self.note1.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.get(id=self.note1.id).name, 'UpdatedNote')

    def test_delete_note(self):
        response = self.client.delete(reverse('note-detail', kwargs={'pk': self.note1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 1)


class TaskTestCase(APITestCase):

    def setUp(self):
        # Створення суперкористувача для тестів
        self.superuser = User.objects.create_superuser(
            username="MarikLNU_matema11",
            email="matema.group11@gmail.com",
            password="OLGGG1234olggg!!!***1234"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

        # Створення категорій подій
        self.category1 = EventCategory.objects.create(name="Category1", description="Description1")
        self.category2 = EventCategory.objects.create(name="Category2", description="Description2")

        # Створення нотаток
        self.note1 = Note.objects.create(name="Note1", description="Description1")
        self.note2 = Note.objects.create(name="Note2", description="Description2")

        # Створення події
        self.event = Event.objects.create(
            name="TestEvent",
            description="EventDescription",
            is_public=True,
            created_by=self.superuser,
            category=self.category1
        )
        self.event.notes.set([self.note1, self.note2])
        self.event.attendees.add(self.superuser)

        # Створення завдань з використанням правильного часу
        due_date = timezone.make_aware(timezone.datetime(2023, 12, 31, 23, 59))
        self.task1 = Task.objects.create(
            title="Task1",
            description="Description1",
            due_date=due_date,
        )
        self.task2 = Task.objects.create(
            title="Task2",
            description="Description2",
            due_date=due_date,
        )
        self.task1.events.add(self.event)
        self.task2.events.add(self.event)

    def test_create_task(self):
        data = {
            "title": "Task3",
            "description": "Description3",
            "due_date": "2023-12-31T23:59",
            "event": self.event.id
        }
        response = self.client.post(reverse('task-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.get(title="Task3").description, "Description3")

    def test_get_all_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_task(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task1')

    def test_update_task(self):
        data = {
            "title": "UpdatedTask",
            "description": "UpdatedDescription"
        }
        response = self.client.patch(reverse('task-detail', kwargs={'pk': self.task1.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task1.id).title, 'UpdatedTask')

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)



class UserTestCase(APITestCase):

    def setUp(self):
        # Створення тестового користувача
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        # Отримання токену
        response = self.client.post('/auth/jwt/create/', {"username": "testuser", "password": "testpassword"}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_all_users(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_single_user(self):
        response = self.client.get(reverse('create-id', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_patch_user(self):
        new_email = "updated@example.com"
        response = self.client.patch(reverse('create-id', args=[self.user.id]), {"email": new_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)

    def test_delete_user(self):
        response = self.client.delete(reverse('create-id', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_user_not_found(self):
        response = self.client.get(reverse('create-id', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

