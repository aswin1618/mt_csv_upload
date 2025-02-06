from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserData
import pandas as pd
import io

class CsvUploadViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.upload_url = "/api/test/" 
    
    def create_csv_file(self, data):
        df = pd.DataFrame(data)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return SimpleUploadedFile("test.csv", csv_buffer.getvalue().encode("utf-8"), content_type="text/csv")

    def test_upload_valid_csv(self):
        csv_data = [
            {"name": "John Doe", "email": "john@example.com", "age": 30},
            {"name": "Jane Doe", "email": "jane@example.com", "age": 25},
        ]
        file = self.create_csv_file(csv_data)

        response = self.client.post(self.upload_url, {"file": file}, format="multipart")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserData.objects.count(), 2)
        self.assertEqual(response.data["total_saved"], 2)

    def test_upload_duplicate_email(self):
        """Test uploading a CSV file with duplicate emails"""
        UserData.objects.create(name="Existing User", email="existing@example.com", age=40)
        
        csv_data = [
            {"name": "John Doe", "email": "existing@example.com", "age": 30}, 
            {"name": "Jane Doe", "email": "jane@example.com", "age": 25}, 
        ]
        file = self.create_csv_file(csv_data)

        response = self.client.post(self.upload_url, {"file": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserData.objects.count(), 2) 
        self.assertEqual(response.data["duplicates"]["count"], 1)
        self.assertIn("existing@example.com", response.data["duplicates"]["duplicate emails"])

    def test_upload_invalid_file_type(self):
        """Test uploading a non-CSV file"""
        file = SimpleUploadedFile("test.txt", b"invalid content", content_type="text/plain")
        
        response = self.client.post(self.upload_url, {"file": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "file type invalid")

    def test_upload_no_file(self):
        """Test uploading without a file"""
        response = self.client.post(self.upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_upload_invalid_data(self):
        """Test uploading a CSV with invalid data"""
        csv_data = [
            {"name": "", "email": "invalid-email", "age": "not-a-number"},
        ]
        file = self.create_csv_file(csv_data)

        response = self.client.post(self.upload_url, {"file": file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertGreater(len(response.data["errors"]), 0) 

