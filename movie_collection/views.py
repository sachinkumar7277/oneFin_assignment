import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .decoretors import retry
from .models import Collection, Movies, RequestCounter
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, CollectionSerializer, \
    MovieCollectionSerializer
from django.contrib.auth import authenticate, login

load_dotenv()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response({
            "access_token": get_tokens_for_user(user)['access']
        })


class LoginApi(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_name = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=user_name, password=password)
            if user is not None:
                return Response({
                    "message": "Logged in success",
                    "access_token": get_tokens_for_user(user)['access']
                })

        return Response({
            "message": "something gone wrong"
        })


class MoivesList(APIView):
    permission_classes = (IsAuthenticated,)

    def get_movies_by_page(self, page=None):

        if page:
            url = os.environ.get('movie_url') + '?page=' + page
        else:
            url = os.environ.get('movie_url')
        try:
            response = requests.get(url, auth=HTTPBasicAuth(os.environ.get('User_name'), os.getenv('Passwd')))
            if response.status_code == 200:
                data = json.loads(response.content)
                return response
            else:
                raise ValueError('response code is not 200')

        except Exception as e:
            raise ValueError('response code is not 200')

    @retry(times=3, exceptions=(ValueError, TypeError, Exception))
    def get(self, request):
        url = os.environ.get('movie_url')
        page = request.GET.get('page')
        response = self.get_movies_by_page(page=page)
        data = response.json()
        if data.get('error'):
            return Response(data, status=response.status_code)

        if data.get("next"):
            data["next"] = data['next'].replace(url, 'http://127.0.0.1:8000/movies/')

        if data.get("previous"):
            data["previous"] = data['previous'].replace(url, 'http://127.0.0.1:8000/movies/')

        return Response(data)


class CollectionListView(ListAPIView, CreateAPIView, ):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(collections, many=True)
        favourite_genres = Movies.objects.filter(collection__user=request.user).order_by("-created")[:3].values_list(
            "genres", flat=True)
        return Response({"is_success": True, 'status_code': status.HTTP_200_OK,
                         "data": {"collections": serializer.data, "favourite_genres": list(favourite_genres)}})

    def post(self, request):
        serializer = MovieCollectionSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"is_success": True, 'status_code': status.HTTP_200_OK, "uuid": serializer.data["uuid"]})


class CollectionView(UpdateAPIView, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieCollectionSerializer

    def get_object(self, pk):
        try:
            collection = Collection.objects.get(uuid=pk)
            return collection
        except Collection.DoesNotExist:
            return None

    def get(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(collection)
        return Response({"success": True, 'status_code': status.HTTP_200_OK, "data": serializer.data})

    def put(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, 'status_code': status.HTTP_200_OK, "data": serializer.data})
        return Response({"success": False, "status_code": status.HTTP_400_BAD_REQUEST, "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = self.get_object(pk)
        if not collection:
            return Response(status=status.HTTP_404_NOT_FOUND)
        collection.delete()
        return Response(
            {"success": True, 'status_code': status.HTTP_200_OK, "message": "collection deleted successfully"})


class RequestCounterView(CreateAPIView, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request = RequestCounter.objects.all().first()
        if request:
            return Response({"is_success": True, 'status_code': status.HTTP_200_OK, "requests": request.request_count})
        else:
            return Response({"requests": 0})

    def post(self, request):
        request = RequestCounter.objects.all().first()
        if request:
            request.request_count = 0
            request.save()
        return Response(
            {"is_success": True, 'status_code': status.HTTP_200_OK, "message": "request count reset successfully"})
