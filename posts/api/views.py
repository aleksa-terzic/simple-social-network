from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg': 'you are not the author of this post.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        if instance.author == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response({'msg': 'you are not the author of this post.'}, status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_like(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user

    if not post.users_like.filter(pk=user.pk).exists():
        post.users_like.add(user)
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_unlike(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user

    if post.users_like.filter(pk=user.pk).exists():
        post.users_like.remove(user)
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_409_CONFLICT)
