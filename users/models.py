from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Universidade(models.Model):
    nome = models.CharField(max_length=150)
    polo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.polo}"


class Curso(models.Model):
    universidade = models.ForeignKey(
        Universidade, on_delete=models.CASCADE, related_name="cursos"
    )
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome} ({self.universidade.nome})"


class Disciplina(models.Model):
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, related_name="disciplinas"
    )
    nome = models.CharField(max_length=150)
    periodo = models.PositiveIntegerField()
    pre_requisitos = models.ManyToManyField(
        "self", blank=True, symmetrical=False
    )

    def __str__(self):
        return self.nome


class User(AbstractUser):
    name = models.CharField(max_length=100)
    universidade = models.ForeignKey(
        Universidade, on_delete=models.SET_NULL, null=True, blank=True
    )
    curso = models.ForeignKey(
        Curso, on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UsuarioDisciplina(models.Model):
    STATUS_CHOICES = [
        ('concluida', 'Concluída'),
        ('em_andamento', 'Em Andamento'),
        ('pendente', 'Pendente'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="disciplinas_usuario"
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.CASCADE,
        related_name="usuarios"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    class Meta:
        unique_together = ('usuario', 'disciplina')  # Impede duplicação

    def __str__(self):
        return f"{self.usuario.name} - {self.disciplina.nome} ({self.status})"

