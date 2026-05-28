from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import ArtistProfile
from .artist_serializers import (
    ArtistProfileSerializer,
    ArtistProfileCreateSerializer,
    PublicArtistProfileSerializer
)


class ArtistProfileCreateView(generics.CreateAPIView):
    serializer_class = ArtistProfileCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        # Only artists can create profiles
        if request.user.role != 'artist':
            return Response(
                {'error': 'Only artists can create an artist profile!'},
                status=status.HTTP_403_FORBIDDEN
            )
        # Check if profile already exists
        if ArtistProfile.objects.filter(user=request.user).exists():
            return Response(
                {'error': 'Artist profile already exists!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ArtistProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ArtistProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        try:
            return self.request.user.artist_profile
        except ArtistProfile.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Artist profile not found!')

    def update(self, request, *args, **kwargs):
        # Only artists can update their own profile
        if request.user.role != 'artist':
            return Response(
                {'error': 'Only artists can update artist profile!'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class PublicArtistListView(generics.ListAPIView):
    serializer_class = PublicArtistProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ArtistProfile.objects.all()


class PublicArtistDetailView(generics.RetrieveAPIView):
    serializer_class = PublicArtistProfileSerializer
    permission_classes = [AllowAny]
    queryset = ArtistProfile.objects.all()


class ArtistProfileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            profile = request.user.artist_profile
            profile.delete()
            return Response(
                {'message': 'Artist profile deleted successfully!'},
                status=status.HTTP_200_OK
            )
        except ArtistProfile.DoesNotExist:
            return Response(
                {'error': 'Artist profile not found!'},
                status=status.HTTP_404_NOT_FOUND
            )
