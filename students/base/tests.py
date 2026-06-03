from django.test import TestCase
from django.urls import reverse
from base.models import Student

class StudentCRUDTests(TestCase):
    def test_create_student(self):
        # Create student via POST
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'age': 20,
            'grade': 'A',
            'gender': 'Male',
            'mobile_number': '1234567890',
            'location': 'New York'
        })
        # Check redirect to home
        self.assertRedirects(response, reverse('home'))
        
        # Verify student exists in database
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.name, 'John Doe')

    def test_read_students(self):
        # Create a test student directly
        Student.objects.create(
            name='Jane Doe', age=22, grade='B', gender='Female',
            mobile_number='9876543210', location='Los Angeles'
        )
        # Fetch home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')

    def test_update_student(self):
        # Create test student
        student = Student.objects.create(
            name='Jane Doe', age=22, grade='B', gender='Female',
            mobile_number='9876543210', location='Los Angeles'
        )
        # Update via POST
        response = self.client.post(reverse('update_student', args=[student.id]), {
            'name': 'Jane Updated',
            'age': 23,
            'grade': 'A',
            'gender': 'Female',
            'mobile_number': '9876543210',
            'location': 'San Francisco'
        })
        self.assertRedirects(response, reverse('home'))
        
        # Verify update
        student.refresh_from_db()
        self.assertEqual(student.name, 'Jane Updated')
        self.assertEqual(student.age, 23)

    def test_delete_student(self):
        # Create test student
        student = Student.objects.create(
            name='Jane Doe', age=22, grade='B', gender='Female',
            mobile_number='9876543210', location='Los Angeles'
        )
        # Delete via POST
        response = self.client.post(reverse('delete_student', args=[student.id]))
        self.assertRedirects(response, reverse('home'))
        
        # Verify deleted
        self.assertEqual(Student.objects.count(), 0)

    def test_advanced_search_filtering(self):
        # Create some test students
        Student.objects.create(name='Alice Smith', age=20, grade='A', gender='Female', mobile_number='111', location='Boston')
        Student.objects.create(name='Bob Jones', age=22, grade='B', gender='Male', mobile_number='222', location='Chicago')
        
        # Test search by name
        response = self.client.get(reverse('home'), {'name': 'Alice'})
        self.assertContains(response, 'Alice Smith')
        self.assertNotContains(response, 'Bob Jones')
        
        # Test search by age
        response = self.client.get(reverse('home'), {'age': '22'})
        self.assertContains(response, 'Bob Jones')
        self.assertNotContains(response, 'Alice Smith')
        
        # Test search by grade
        response = self.client.get(reverse('home'), {'grade': 'A'})
        self.assertContains(response, 'Alice Smith')
        self.assertNotContains(response, 'Bob Jones')

        # Test search by gender
        response = self.client.get(reverse('home'), {'gender': 'Male'})
        self.assertContains(response, 'Bob Jones')
        self.assertNotContains(response, 'Alice Smith')

        # Test search by location
        response = self.client.get(reverse('home'), {'location': 'Chicago'})
        self.assertContains(response, 'Bob Jones')
        self.assertNotContains(response, 'Alice Smith')
