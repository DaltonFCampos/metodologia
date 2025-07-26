from rest_framework import serializers

from .models import Curso, Disciplina, Universidade, User, UsuarioDisciplina


class UniversidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidade
        fields = ['id', 'nome', 'polo']


class CursoSerializer(serializers.ModelSerializer):
    universidade = UniversidadeSerializer(read_only=True)
    universidade_id = serializers.PrimaryKeyRelatedField(
        queryset=Universidade.objects.all(),
        source='universidade',
        write_only=True
    )

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'universidade', 'universidade_id']


class DisciplinaSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'periodo', 'curso', 'pre_requisitos', 'status']

    def get_status(self, obj):
        """Retorna o status do usuário autenticado para a disciplina."""
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        usuario_disciplina = UsuarioDisciplina.objects.filter(usuario=user, disciplina=obj).first()
        return usuario_disciplina.status if usuario_disciplina else "pendente"




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(
        queryset=Universidade.objects.all(), source='universidade'
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso'
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'email', 'password', 'confirmPassword',
            'university', 'city', 'course'
        ]
        extra_kwargs = {
            'username': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirmPassword'):
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        password = validated_data.pop('password')
        user = User(**validated_data)
        # Gerar username baseado no email
        user.username = validated_data['email']
        user.set_password(password)
        user.save()
        return user

class UsuarioDisciplinaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.CharField(source='disciplina.nome', read_only=True)

    class Meta:
        model = UsuarioDisciplina
        fields = ['id', 'usuario', 'disciplina', 'disciplina_nome', 'status']
        extra_kwargs = {
            'usuario': {'read_only': True}
        }

    def validate(self, attrs):
        user = self.context['request'].user
        disciplina = attrs.get('disciplina')
        status = attrs.get('status')

        if status == 'concluida':
            prerequisitos = disciplina.pre_requisitos.all()
            for pre in prerequisitos:
                if not UsuarioDisciplina.objects.filter(
                    usuario=user,
                    disciplina=pre,
                    status='concluida'
                ).exists():
                    raise serializers.ValidationError(
                        {"status": f"Não é possível concluir '{disciplina.nome}' sem concluir o pré-requisito '{pre.nome}'."}
                    )

        return attrs

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)