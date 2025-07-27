from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['patch'], url_path='update-status')
    def update_status(self, request):
        disciplina_id = request.data.get('disciplina')
        status_value = request.data.get('status')

        # Validação de campos obrigatórios
        if not disciplina_id or not status_value:
            return Response(
                {"detail": "Campos 'disciplina' e 'status' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obter disciplina e validar pré-requisitos
        try:
            disciplina = Disciplina.objects.get(pk=disciplina_id)
        except Disciplina.DoesNotExist:
            return Response(
                {"detail": "Disciplina não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        if status_value == "concluida":
            prerequisitos = disciplina.pre_requisitos.all()
            for pre in prerequisitos:
                if not UsuarioDisciplina.objects.filter(
                    usuario=request.user,
                    disciplina=pre,
                    status="concluida"
                ).exists():
                    return Response(
                        {"detail": f"Não é possível concluir '{disciplina.nome}' sem concluir o pré-requisito '{pre.nome}'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # Cria ou atualiza o registro
        obj, created = UsuarioDisciplina.objects.update_or_create(
            usuario=request.user,
            disciplina=disciplina,
            defaults={'status': status_value}
        )

        serializer = self.get_serializer(obj)
        return Response(serializer.data)