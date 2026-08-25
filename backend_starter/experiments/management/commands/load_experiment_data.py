import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from experiments.models import Experiment, ExposureBand, DayConversion, HourConversion


class Command(BaseCommand):
    help = (
        "Carga experiment_summary.csv, statistical_results.csv, "
        "experiment_decision.json, exposure_analysis.csv, "
        "conversion_by_day.csv y conversion_by_hour.csv "
        "(copiados de data/processed/ del proyecto ux_ab_testing_analysis_complete) "
        "a la base de datos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help="Carpeta que contiene los 6 archivos. Por defecto: backend/data/",
        )

    def handle(self, *args, **options):
        data_dir = Path(options['data_dir'])

        for fname in [
            'experiment_summary.csv', 'statistical_results.csv',
            'experiment_decision.json', 'exposure_analysis.csv',
            'conversion_by_day.csv', 'conversion_by_hour.csv',
        ]:
            if not (data_dir / fname).exists():
                self.stderr.write(self.style.ERROR(
                    f"No se encontró {data_dir / fname}. "
                    f"Copia los 6 archivos de data/processed/ del repo original a {data_dir}/"
                ))
                return

        # --- 1. statistical_results.csv -> dict metric: value ---
        stats = {}
        with open(data_dir / 'statistical_results.csv', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                stats[row['metric']] = float(row['value'])

        # --- 2. experiment_summary.csv -> dict test_group: fila ---
        summary = {}
        with open(data_dir / 'experiment_summary.csv', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                summary[row['test_group']] = row

        # --- 3. experiment_decision.json ---
        with open(data_dir / 'experiment_decision.json', encoding='utf-8') as f:
            decision = json.load(f)

        # --- 4. Crear o actualizar el Experiment ---
        experiment, created = Experiment.objects.update_or_create(
            name="UX A/B Testing — Marketing Campaign (ad vs psa)",
            defaults=dict(
                users_treatment=int(float(summary['ad']['users'])),
                users_control=int(float(summary['psa']['users'])),
                conversions_treatment=int(float(summary['ad']['conversions'])),
                conversions_control=int(float(summary['psa']['conversions'])),
                conversion_rate_treatment=stats['treatment_conversion_rate'],
                conversion_rate_control=stats['control_conversion_rate'],
                absolute_uplift=stats['absolute_uplift'],
                relative_uplift=stats['relative_uplift'],
                z_statistic=stats['z_statistic'],
                z_p_value=stats['z_p_value'],
                chi_square=stats['chi_square'],
                chi_square_p_value=stats['chi_square_p_value'],
                ci_difference_low=stats['ci_difference_low'],
                ci_difference_high=stats['ci_difference_high'],
                bootstrap_ci_low=stats['bootstrap_ci_low'],
                bootstrap_ci_high=stats['bootstrap_ci_high'],
                risk_ratio=stats['risk_ratio'],
                risk_ratio_ci_low=stats['risk_ratio_ci_low'],
                risk_ratio_ci_high=stats['risk_ratio_ci_high'],
                cohen_h=stats['cohen_h'],
                observed_power=stats['observed_power'],
                logistic_odds_ratio=stats['logistic_odds_ratio'],
                logistic_or_ci_low=stats['logistic_or_ci_low'],
                logistic_or_ci_high=stats['logistic_or_ci_high'],
                alpha=decision['alpha'],
                decision=decision['decision'],
                statistically_significant=decision['statistically_significant'],
                methodological_note=decision.get('methodological_note', ''),
            ),
        )

        # --- 5. Limpiar comportamiento previo (por si se re-ejecuta el comando) ---
        experiment.exposure_bands.all().delete()
        experiment.day_conversions.all().delete()
        experiment.hour_conversions.all().delete()

        # --- 6. exposure_analysis.csv ---
        with open(data_dir / 'exposure_analysis.csv', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                ExposureBand.objects.create(
                    experiment=experiment,
                    exposure_band=row['exposure_band'],
                    users=int(float(row['users'])),
                    conversions=int(float(row['conversions'])),
                    conversion_rate_pct=float(row['conversion_rate_pct']),
                    avg_ads=float(row['avg_ads']),
                )

        # --- 7. conversion_by_day.csv ---
        with open(data_dir / 'conversion_by_day.csv', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                DayConversion.objects.create(
                    experiment=experiment,
                    day=row['most_ads_day'],
                    users=int(float(row['users'])),
                    conversions=int(float(row['conversions'])),
                    conversion_rate_pct=float(row['conversion_rate_pct']),
                    avg_ads=float(row['avg_ads']),
                )

        # --- 8. conversion_by_hour.csv ---
        with open(data_dir / 'conversion_by_hour.csv', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                HourConversion.objects.create(
                    experiment=experiment,
                    hour=int(float(row['most_ads_hour'])),
                    users=int(float(row['users'])),
                    conversions=int(float(row['conversions'])),
                    conversion_rate_pct=float(row['conversion_rate_pct']),
                    avg_ads=float(row['avg_ads']),
                )

        accion = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(
            f"Experimento {accion}: '{experiment.name}'\n"
            f"  - {experiment.exposure_bands.count()} bandas de exposición\n"
            f"  - {experiment.day_conversions.count()} días\n"
            f"  - {experiment.hour_conversions.count()} horas"
        ))
