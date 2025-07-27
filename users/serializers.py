from rest_framework import serializers

from .models import Curso, Disciplina, Universidade, User, UsuarioDisciplina


class UniversidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidade
        fields = ["id", "nome", "polo"]


class CursoSerializer(serializers.ModelSerializer):
    universidade = UniversidadeSerializer(read_only=True)
    universidade_id = serializers.PrimaryKeyRelatedField(
        queryset=Universidade.objects.all(),
        source="universidade",
        write_only=True,
    )

    class Meta:
        model = Curso
        fields = ["id", "nome", "universidade", "universidade_id"]


class DisciplinaSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Disciplina
        fields = ["id", "nome", "periodo", "curso", "pre_requisitos", "status"]

    def get_status(self, obj):
        """Retorna o status do usuário autenticado para a disciplina."""
        user = self.context["request"].user
        if not user.is_authenticated:
            return None
        usuario_disciplina = UsuarioDisciplina.objects.filter(
            usuario=user, disciplina=obj
        ).first()
        return usuario_disciplina.status if usuario_disciplina else "pendente"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(
        queryset=Universidade.objects.all(), source="universidade"
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source="curso"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "password",
            "confirmPassword",
            "university",
            "city",
            "course",
        ]
        extra_kwargs = {"username": {"read_only": True}}

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirmPassword"):
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        password = validated_data.pop("password")
        user = User(**validated_data)
        # Gerar username baseado no email
        user.username = validated_data["email"]
        user.set_password(password)
        user.save()
        return user


class UsuarioDisciplinaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.CharField(source="disciplina.nome", read_only=True)

    class Meta:
        model = UsuarioDisciplina
        fields = ["id", "usuario", "disciplina", "disciplina_nome", "status"]
        extra_kwargs = {"usuario": {"read_only": True}}

    def create(self, validated_data):
        """
        Cria ou atualiza o status da disciplina para o usuário autenticado.
        (A validação de pré-requisitos agora é feita no viewset.)
        """
        user = self.context["request"].user
        disciplina = validated_data.get("disciplina")

        obj, created = UsuarioDisciplina.objects.update_or_create(
            usuario=user,
            disciplina=disciplina,
            defaults={"status": validated_data.get("status", "pendente")},
        )
        return obj