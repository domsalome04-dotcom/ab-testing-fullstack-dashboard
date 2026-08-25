from rest_framework import serializers
from .models import Experiment, ExposureBand, DayConversion, HourConversion


class ExposureBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExposureBand
        fields = ['id', 'exposure_band', 'users', 'conversions', 'conversion_rate_pct', 'avg_ads']


class DayConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayConversion
        fields = ['id', 'day', 'users', 'conversions', 'conversion_rate_pct', 'avg_ads']


class HourConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourConversion
        fields = ['id', 'hour', 'users', 'conversions', 'conversion_rate_pct', 'avg_ads']


class ExperimentListSerializer(serializers.ModelSerializer):
    """
    Versión ligera para GET /api/experiments/
    No incluye los datos de comportamiento anidados, para que listar
    varios experimentos no traiga cientos de filas innecesarias.
    """
    class Meta:
        model = Experiment
        fields = [
            'id', 'name',
            'users_treatment', 'users_control',
            'conversion_rate_treatment', 'conversion_rate_control',
            'absolute_uplift', 'relative_uplift', 'z_p_value',
            'decision', 'statistically_significant', 'created_at',
        ]


class ExperimentDetailSerializer(serializers.ModelSerializer):
    """
    Versión completa para GET /api/experiments/{id}/
    y para POST / PATCH / PUT.
    Incluye las tres tablas de comportamiento anidadas (solo lectura).
    """
    exposure_bands = ExposureBandSerializer(many=True, read_only=True)
    day_conversions = DayConversionSerializer(many=True, read_only=True)
    hour_conversions = HourConversionSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment
        fields = '__all__'
