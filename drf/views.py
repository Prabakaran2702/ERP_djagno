from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

# Create your views here.

class ProductView(APIView):

    def get(self, request):
        print('GET')
        Books = Book.objects.all()
        serializer = BookSerializer(Books, many=True)
        return Response({'message': 'GET METHOD WORKING',
                         'data':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        print('POST')
        data = request.data 
        print(data,'<------->')

        # Save Multiple data
        if isinstance(data, list):  # Check if the data is a list
            serializers = [BookSerializer(data=item) for item in data]
            valid = all([serializer.is_valid() for serializer in serializers])

            if valid:
                for serializer in serializers:
                    serializer.save()
                return Response({'message': 'POST METHOD WORKING',
                                 'data': [serializer.data for serializer in serializers]}, status=status.HTTP_201_CREATED)
            else:
                error_messages = [serializer.errors for serializer in serializers if not serializer.is_valid()]
                return Response({'message': 'POST METHOD FAILED',
                                 'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            
        # Save single data
        else:            
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'POST METHOD WORKING',
                            'data':serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'message': 'POST METHOD Failed',
                            'data':serializer.data}, status=status.HTTP_400_BAD_REQUEST)
        
        
    
    def put(self, request):
        print('PUT')

        book_id = request.data.get('id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'PUT METHOD WORKING', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'PUT METHOD Failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request):
        print('PATCH')
        book_id = request.data.get('id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update specific fields of the book instance with new data
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'PATCH METHOD WORKING', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'PATCH METHOD Failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request):
        print('DELETE')

        book_id = request.data.get('id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({'message': 'DELETE METHOD WORKING', 'data': f'Book with id {book_id} deleted successfully'}, status=status.HTTP_200_OK)


class BookListCreate(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer