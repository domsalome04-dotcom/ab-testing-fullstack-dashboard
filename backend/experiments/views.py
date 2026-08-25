from rest_framework import viewsets
from .models import Experiment
from .serializers import ExperimentListSerializer, ExperimentDetailSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    """
    Provee automáticamente:
      GET    /api/experiments/         -> listar (versión ligera)
      POST   /api/experiments/         -> crear
      GET    /api/experiments/{id}/    -> detalle (con comportamiento anidado)
      PUT    /api/experiments/{id}/    -> reemplazar completo
      PATCH  /api/experiments/{id}/    -> actualizar parcial (ej. cambiar 'decision')
      DELETE /api/experiments/{id}/    -> eliminar
    """
    queryset = Experiment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExperimentListSerializer
        return ExperimentDetailSerializer
