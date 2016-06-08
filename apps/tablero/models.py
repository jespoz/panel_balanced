# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Perspectiva(models.Model):
    descripcion = models.CharField(max_length=50)
    peso = models.FloatField(default=0, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        verbose_name = 'Dimension'
        verbose_name_plural = 'Dimensiones'

    def __unicode__(self):
        return self.descripcion


class Objetivo(models.Model):
    descripcion = models.TextField()
    perspectiva = models.ForeignKey(Perspectiva)

    def __unicode__(self):
        return self.descripcion


class Unidad(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Unidades'

    def __unicode__(self):
        return self.descripcion


class Periodo(models.Model):
    descripcion = models.CharField(max_length=50)

    def __unicode__(self):
        return self.descripcion


class AdministradorUnidad(models.Model):
    unidad = models.OneToOneField(Unidad, unique=True)
    administrador = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Administrador de Unidad'
        verbose_name_plural = 'Administradores de Unidad'

    def __unicode__(self):
        return '%s (%s)' % (self.unidad, self.administrador)


class Color(models.Model):
    color = models.CharField(max_length=50)
    hexadecimal = models.CharField(max_length=7)

    class Meta:
        verbose_name_plural = 'Colores'

    def __unicode__(self):
        return self.color


class Semaforo(models.Model):
    desde = models.FloatField(default=0)
    hasta = models.FloatField(default=0)
    color = models.ForeignKey(Color)

    def __unicode__(self):
        return '%s - %s al %s' % (self.color, self.desde, self.hasta)


class Proyecto(models.Model):
    nombre = models.TextField()
    objetivo = models.ForeignKey(Objetivo)
    lider = models.ForeignKey(User, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, null=True, blank=True)

    def __unicode__(self):
        return self.nombre


class IndicadorObjetivo(models.Model):
    descripcion = models.CharField(max_length=100)
    objetivo = models.ForeignKey(Objetivo)
    responsable = models.ForeignKey(User, null=True, blank=True)
    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Indicador por Objetivo'
        verbose_name_plural = 'Indicadores por Objetivo'

    def __unicode__(self):
        return self.descripcion


class TipoAperturaIndicador(models.Model):
    indicador = models.ForeignKey(IndicadorObjetivo)
    apertura = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tipo de Apertura por Indicador'
        verbose_name_plural = 'Tipos de Aperturas por Indicador'

    def __unicode__(self):
        return '%s: %s' % (self.indicador, self.apertura)


class ResultadoIndicador(models.Model):
    indicador = models.ForeignKey(TipoAperturaIndicador)
    periodo = models.ForeignKey(Periodo)
    meta = models.FloatField(default=0)
    resultado = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Resultado indicadores'

    def __unicode__(self):
        return '%s - %s' % (self.periodo, self.indicador)


class TotalIndicador(models.Model):
    indicador = models.ForeignKey(IndicadorObjetivo)
    periodo = models.ForeignKey(Periodo)
    meta = models.FloatField(default=0)
    resultado = models.FloatField(default=0)
    cumplimiento = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Total indicadores'

    def __unicode__(self):
        return '%s - %s' % (self.periodo, self.indicador)


class TotalDimension(models.Model):
    indicador = models.ForeignKey(Perspectiva)
    periodo = models.ForeignKey(Periodo)
    resultado = models.FloatField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.periodo, self.indicador)


class Status(models.Model):
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Status'

    def __unicode__(self):
        return self.descripcion


class KPI(models.Model):
    proyecto = models.ForeignKey(Proyecto)
    descripcion = models.CharField(max_length=150)
    meta = models.CharField(max_length=50, default=0, null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True)
    evaluacion = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'KPI'

    def __unicode__(self):
        return self.descripcion


class Escala(models.Model):
    nombre = models.CharField(max_length=50)
    desde = models.FloatField(default=0)
    hasta = models.FloatField(default=0)
    color = models.ForeignKey(Color)

    def __unicode__(self):
        return self.nombre


class Ciclo(models.Model):
    ciclo = models.CharField(max_length=50)
    fecha = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.ciclo


class Revision(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    proyecto = models.ForeignKey(Proyecto)
    observacion = models.TextField(null=True, blank=True)
    avance = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Avances de Ciclos'

    def __unicode__(self):
        return 'Ciclo %s - %s' % (self.ciclo, self.proyecto)


class TotalCicloUnidad(models.Model):
    ciclo = models.ForeignKey(Ciclo)
    unidad = models.ForeignKey(Unidad)
    avance = models.FloatField(default=0)
