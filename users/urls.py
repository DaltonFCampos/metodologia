from rest_framework.routers import DefaultRouter

from .viewsets import (CursoViewSet, DisciplinaViewSet, UniversidadeViewSet,
                       UserViewSet, UsuarioDisciplinaViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'universidades', UniversidadeViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'usuario-disciplinas', UsuarioDisciplinaViewSet)

urlpatterns = router.urls
