from django.db import models


class Experiment(models.Model):
    """
    Registro principal de un experimento A/B.
    Corresponde a experiment_summary.csv + statistical_results.csv +
    experiment_decision.json del proyecto ux_ab_testing_analysis_complete.
    """
    name = models.CharField(max_length=200)

    # --- Muestra (experiment_summary.csv) ---
    users_treatment = models.IntegerField()
    users_control = models.IntegerField()
    conversions_treatment = models.IntegerField()
    conversions_control = models.IntegerField()

    # --- Tasas y efecto (statistical_results.csv) ---
    conversion_rate_treatment = models.FloatField()
    conversion_rate_control = models.FloatField()
    absolute_uplift = models.FloatField()
    relative_uplift = models.FloatField()

    # --- Prueba de hipótesis ---
    z_statistic = models.FloatField()
    z_p_value = models.FloatField()
    chi_square = models.FloatField()
    chi_square_p_value = models.FloatField()

    # --- Intervalos de confianza ---
    ci_difference_low = models.FloatField()
    ci_difference_high = models.FloatField()
    bootstrap_ci_low = models.FloatField()
    bootstrap_ci_high = models.FloatField()

    # --- Tamaño de efecto y potencia ---
    risk_ratio = models.FloatField()
    risk_ratio_ci_low = models.FloatField()
    risk_ratio_ci_high = models.FloatField()
    cohen_h = models.FloatField()
    observed_power = models.FloatField()
    logistic_odds_ratio = models.FloatField()
    logistic_or_ci_low = models.FloatField()
    logistic_or_ci_high = models.FloatField()

    # --- Decisión (experiment_decision.json) ---
    alpha = models.FloatField(default=0.05)
    decision = models.CharField(max_length=50)
    statistically_significant = models.BooleanField(default=False)
    methodological_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ExposureBand(models.Model):
    """Corresponde a exposure_analysis.csv"""
    experiment = models.ForeignKey(
        Experiment, related_name='exposure_bands', on_delete=models.CASCADE
    )
    exposure_band = models.CharField(max_length=50)   # ej. "1-10", "11-25"
    users = models.IntegerField()
    conversions = models.IntegerField()
    conversion_rate_pct = models.FloatField()
    avg_ads = models.FloatField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.experiment.name} · {self.exposure_band}"


class DayConversion(models.Model):
    """Corresponde a conversion_by_day.csv"""
    experiment = models.ForeignKey(
        Experiment, related_name='day_conversions', on_delete=models.CASCADE
    )
    day = models.CharField(max_length=20)   # ej. "Monday"
    users = models.IntegerField()
    conversions = models.IntegerField()
    conversion_rate_pct = models.FloatField()
    avg_ads = models.FloatField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.experiment.name} · {self.day}"


class HourConversion(models.Model):
    """Corresponde a conversion_by_hour.csv"""
    experiment = models.ForeignKey(
        Experiment, related_name='hour_conversions', on_delete=models.CASCADE
    )
    hour = models.IntegerField()   # 0-23
    users = models.IntegerField()
    conversions = models.IntegerField()
    conversion_rate_pct = models.FloatField()
    avg_ads = models.FloatField()

    class Meta:
        ordering = ['hour']

    def __str__(self):
        return f"{self.experiment.name} · {self.hour}:00"
