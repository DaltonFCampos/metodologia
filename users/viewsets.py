from rest_framework import permissions, viewsets

from .models import Curso, Disciplina, Universidade, User, UsuarioDisciplina
from .serializers import (CursoSerializer, DisciplinaSerializer,
                          UniversidadeSerializer, UserSerializer,
                          UsuarioDisciplinaSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UniversidadeViewSet(viewsets.ModelViewSet):
    queryset = Universidade.objects.all()
    serializer_class = UniversidadeSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer




class UsuarioDisciplinaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioDisciplina.objects.all()
    serializer_class = UsuarioDisciplinaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UsuarioDisciplina.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)