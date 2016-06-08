from django.contrib import admin
from .models import *


@admin.register(Perspectiva)
class PerspectivaAdmin(admin.ModelAdmin):
    pass


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['perspectiva', 'descripcion']
    list_filter = ['perspectiva']


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    pass


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    pass


@admin.register(AdministradorUnidad)
class AdministradorUnidadAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'administrador']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Semaforo)
class SemaforoAdmin(admin.ModelAdmin):
    pass


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lider']
    list_filter = ['objetivo__perspectiva', 'unidad', 'lider']


@admin.register(IndicadorObjetivo)
class IndicadorObjetivoAdmin(admin.ModelAdmin):
    pass


@admin.register(TipoAperturaIndicador)
class TipoAperturaIndicadorAdmin(admin.ModelAdmin):
    pass


@admin.register(ResultadoIndicador)
class ResultadoIndicadorAdmin(admin.ModelAdmin):
    pass


@admin.register(TotalIndicador)
class TotalIndicadorAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


# @admin.register(TotalDimension)
# class TotalDimensionAdmin(admin.ModelAdmin):
#     pass


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    pass


@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    pass


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    pass


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'avance', 'get_lider', 'get_unidad', ]
    list_filter = ('ciclo', 'proyecto__unidad', )

    def get_lider(self, obj):
        return obj.proyecto.lider

    def get_unidad(self, obj):
        return obj.proyecto.unidad

    get_lider.short_description = 'Lider'
    get_unidad.short_description = 'Unidad'
