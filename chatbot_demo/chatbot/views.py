# from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import *
from .langchain_bot import get_answer_from_index_with_memory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Chat(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'session_id', openapi.IN_QUERY, description="ID of the chat session",
                type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'doc_theme_name', openapi.IN_QUERY, description="Name of the theme user is consulting",
                type=openapi.TYPE_STRING, required=True
            ),
            openapi.Parameter(
                'max_context_messages', openapi.IN_QUERY, description="Maximum number of context messages to consider",
                type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'question', openapi.IN_QUERY, description="Question for chatbot",
                type=openapi.TYPE_STRING, required=True
            )            
        ]
    )

    def post(self, request):
        # Extract query parameters and pass them to the serializer
        data = {
            "session_id": request.query_params.get("session_id"),
            "doc_theme_name": request.query_params.get("doc_theme_name"),
            "max_context_messages": request.query_params.get("max_context_messages"),
            "question": request.query_params.get("question")
        }

        # Use the serializer to validate and parse data
        serializer = ChatRequestSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        session_id = serializer.validated_data.get("session_id")
        index_name = serializer.validated_data.get("doc_theme_name")
        max_context_messages = serializer.validated_data.get("max_context_messages")
        question = serializer.validated_data.get("question")

        try:
            # Get the answer using the provided parameters
            answer = get_answer_from_index_with_memory(question, index_name, session_id, max_context_messages)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Messages(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'session_id', openapi.IN_QUERY, description="ID of the chat session",
                type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'user_id', openapi.IN_QUERY, description="ID of the user",
                type=openapi.TYPE_INTEGER, required=False
            )
        ]
    )

    def get(self, request):
        # Get query parameters
        session_id = request.query_params.get("session_id")
        user_id = request.query_params.get("user_id")

        # Build the query filters dynamically
        filters = {}

        # Add filter for session_id if provided
        if session_id:
            try:
                # Check if the session exists
                ChatSession.objects.get(id=session_id)
                filters['session_id'] = session_id
            except ChatSession.DoesNotExist:
                return Response({"error": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Add filter for user_id if provided
        if user_id:
            try:
                # Check if the user exists
                User.objects.get(id=user_id)
                filters['session__user_id'] = user_id
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Apply filters directly to the queryset
            messages = ChatMessage.objects.filter(**filters)

            # Serialize and return the filtered messages
            serializer = ChatMessagesSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Catch any other unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Session(APIView):
    
    def get(self, request):
        sessions = ChatSession.objects.all()
        sessions_list = [{"id": session.id,
                          "user": session.user.username,
                          "created_at": session.created_at,
                          "updated_at": session.updated_at,} for session in sessions]
        return Response({"themes": sessions_list}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY, description="ID of the user",
                type=openapi.TYPE_INTEGER, required=True
            )
        ],
        responses={
            200: "New chat session created successfully",
            400: "Invalid input or missing parameters",
            404: "User not found"
        }
    )
    def post(self, request):
        # Extract user id
        user_id = request.query_params.get("user_id")

        # Validate that the user_id is provided
        if not user_id:
            return Response({"error": "User id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # get user who is stating the session
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Create new Chat Session 
        new_session = ChatSession.objects.create(user=user)

        return Response({"id": new_session.id,
                         "user": new_session.user.username,
                         "created_at": new_session.created_at,
                         "updated_at": new_session.updated_at}, status=status.HTTP_200_OK)

class Partitions(APIView):
    def get(self, request):
        partitions = PartitonPypes.objects.all()
        partitions_list = [{"id": partition.id, 
                        "type": partition.type} for partition in partitions]
        return Response({"partitions": partitions_list}, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Extract the partition name from the request data
        partition_name = request.data.get("type")
        
        # Validate that the partition name is provided
        if not partition_name:
            return Response({"error": "Parition name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a partition with the same name already exists (optional)
        if PartitonPypes.objects.filter(type=partition_name).exists():
            return Response({"error": "Partition with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new partition and save it to the database
        new_partition = PartitonPypes.objects.create(type=partition_name)
        
        # Return the created partition's details
        return Response({"id": new_partition.id, "type": new_partition.type}, status=status.HTTP_201_CREATED)

class Themes(APIView):
    def get(self, request):
        themes = DocThemes.objects.all()
        themes_list = [{"id": theme.id, 
                        "theme": theme.theme} for theme in themes]
        return Response({"themes": themes_list}, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Extract the theme name from the request data
        theme_name = request.data.get("theme")
        
        # Validate that the theme name is provided
        if not theme_name:
            return Response({"error": "Theme name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a theme with the same name already exists (optional)
        if DocThemes.objects.filter(theme=theme_name).exists():
            return Response({"error": "Theme with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new theme and save it to the database
        new_theme = DocThemes.objects.create(theme=theme_name)
        
        # Return the created theme's details
        return Response({"id": new_theme.id, "theme": new_theme.theme}, status=status.HTTP_201_CREATED)
