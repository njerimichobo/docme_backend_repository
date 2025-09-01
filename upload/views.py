import tempfile
import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Upload
from .serializers import UploadSerializer
from rest_framework import viewsets
from pymupdf4llm import to_markdown
# Assuming this is the correct import for your LLM function
from .llm_chain import run_flow
from .llm_cleaner import parse_llm_text
import re
import ast
import json
from rest_framework.decorators import action


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        uploaded_file = serializer.instance.file

        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Write the file content to temp file
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

            raw_text = to_markdown(temp_path)

            print("Raw text extracted from PDF:", raw_text)

            name_match = re.search(
                r"# Patient Name:\s*(.*?)(?:\s+Date of Birth|$)", raw_text)

            id_match = re.search(r"Patient ID:\s*(\d+)", raw_text)
            report_date_match = re.search(
                r"Date of Test:\s*(\d{4}-\d{2}-\d{2})", raw_text)

            patient_metadata = {
                "name": name_match.group(1).strip() if name_match else None,
                "id": id_match.group(1).strip() if id_match else None,
                "reportDate": report_date_match.group(1).strip() if report_date_match else None
            }

            print("Patient Metadata:", patient_metadata)

            try:
                llm_result = run_flow(raw_text)

            except Exception as e:
                print(f"Error in run_flow: {e}")
                return Response({"error": "Error during text processing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if os.path.exists(temp_path):
                os.remove(temp_path)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        report_instance = serializer.instance
        report_instance.patient_name = patient_metadata["name"]
        report_instance.patient_id = patient_metadata["id"]
        report_instance.report_date = patient_metadata["reportDate"]
        report_instance.llm_result = llm_result
        report_instance.save()

        return Response({
            "id": serializer.instance.id,
            "file": serializer.instance.file.url,
            "patient": patient_metadata,
            "llm_result": llm_result,
        }, status=status.HTTP_201_CREATED)\


    @action(detail=True, methods=['get'])
    def retrieve_report(self, request, pk=None):
        try:
            # Fetch the uploaded report by ID (pk)
            report = Upload.objects.get(pk=pk)

            return Response({
                "id": report.id,
                "file": report.file.url,
                "patient": {
                    "name": report.patient_name,
                    "id": report.patient_id,
                    "reportDate": report.report_date,
                },
                "llm_result": report.llm_result,
            })

        except Upload.DoesNotExist:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)
