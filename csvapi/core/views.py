from django.shortcuts import render
from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import pandas as pd
from .serializers import UserDataSerializer
from .models import UserData
# Create your views here.


class CsvUploadView(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        
        if not file:
            return Response({"error":"no file specified"},status=status.HTTP_400_BAD_REQUEST)
        if not file.name.endswith('.csv'):
            return Response({"error":"file type invalid"},status=status.HTTP_400_BAD_REQUEST)
        
        df= pd.read_csv(file)
        
        errors = []
        rejected_count = 0
        skipped_count = 0  
        saved_count = 0
        skipped_emails = []

        for index, row in df.iterrows():
            name = row['name']
            email = row['email']
            age = row['age']
            
            if UserData.objects.filter(email=email).exists():
                skipped_count += 1
                skipped_emails.append(email)
                continue 

            data = {"name": name, "email": email, "age": age}
            serializer = UserDataSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                saved_count += 1
            else:
                rejected_count += 1
                errors.append(
                    {
                        "row": index + 1, 
                        "email": email,
                        "errors": serializer.errors,
                    }
                )

        return Response(
            {
                "message": "File processed successfully.",
                "total_saved": saved_count,
                "duplicates": {"count":skipped_count, "duplicate emails":skipped_emails},
                "total_rejected": rejected_count,
                "errors": errors,  # List of error messages
            },
            status=status.HTTP_201_CREATED if saved_count > 0 else status.HTTP_400_BAD_REQUEST,
        )
        