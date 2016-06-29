from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, DetailView
from django.db.models import Avg

from .models import *

import json


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['perspectivas'] = []
        periodo = 0
        total = 0
        anterior = 0
        context['periodo'] = Periodo.objects.all().order_by('-id')[:1]
        for i in context['periodo']:
            periodo = i.id
        resultados = TotalDimension.objects.values(
            'indicador_id', 'resultado', 'id').filter(periodo_id=periodo)
        perspectivas = Perspectiva.objects.values(
            'id', 'descripcion', 'peso', 'color')
        for x in perspectivas:
            for i in resultados:
                if (x['id'] == i['indicador_id']):
                    if TotalDimension.objects.all().filter(
                            periodo_id=periodo - 1,
                            indicador_id=x['id']).exists():
                        qs = TotalDimension.objects.values(
                            'resultado').filter(
                            periodo_id=periodo - 1, indicador_id=x['id'])
                        for rs in qs:
                            anterior = round(
                                i['resultado'] - rs['resultado'], 0)
                    else:
                        anterior = 0
                    context['perspectivas'].append({
                        'resultado': i['resultado'],
                        'id': x['id'],
                        'anterior': 0,
                        'color': x['color'],
                        'peso': x['peso'],
                        'descripcion': x['descripcion'],
                        'anterior': anterior
                    })
        for x in resultados:
            if TotalDimension.objects.all().filter(
                    periodo_id=periodo - 1).exists():
                qs = TotalDimension.objects.values(
                    'resultado').filter(periodo_id=periodo - 1)
                for rs in qs:
                    anterior = round(x['resultado'] - rs['resultado'], 0)
            else:
                anterior = 0
            perspectivas = Perspectiva.objects.all().filter(
                id=x['indicador_id']
            )
            for i in perspectivas:
                total += x['resultado'] * i.peso
        semaforo = Semaforo.objects.values(
            'color__hexadecimal', 'desde', 'hasta')
        for x in semaforo:
            if total >= x['desde'] and total <= x['hasta']:
                context['total'] = {
                    'total': str(total),
                    'color': x['color__hexadecimal']
                }
        context['unidades'] = Unidad.objects.all()
        context['ciclos'] = Ciclo.objects.all().order_by('-id')
        context['semaforo'] = Semaforo.objects.values(
            'desde', 'hasta', 'color__hexadecimal'
        )
        return context


class IndexDetailView(DetailView):
    model = Periodo
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['perspectivas'] = []
        periodo = 0
        total = 0
        anterior = 0
        context['periodo'] = Periodo.objects.all().filter(
            id=self.get_object().pk).order_by('-id')[:1]
        for i in context['periodo']:
            periodo = i.id
        resultados = TotalDimension.objects.values(
            'indicador_id', 'resultado', 'id').filter(periodo_id=periodo)
        perspectivas = Perspectiva.objects.values(
            'id', 'descripcion', 'peso', 'color')
        for x in perspectivas:
            for i in resultados:
                if (x['id'] == i['indicador_id']):
                    if TotalDimension.objects.all().filter(
                            periodo_id=periodo - 1,
                            indicador_id=x['id']).exists():
                        qs = TotalDimension.objects.values(
                            'resultado').filter(
                            periodo_id=periodo - 1, indicador_id=x['id'])
                        for rs in qs:
                            anterior = round(
                                i['resultado'] - rs['resultado'], 0)
                    else:
                        anterior = 0
                    context['perspectivas'].append({
                        'resultado': i['resultado'],
                        'id': x['id'],
                        'anterior': 0,
                        'color': x['color'],
                        'peso': x['peso'],
                        'descripcion': x['descripcion'],
                        'anterior': anterior
                    })
        for x in resultados:
            if TotalDimension.objects.all().filter(
                    periodo_id=periodo - 1).exists():
                qs = TotalDimension.objects.values(
                    'resultado').filter(periodo_id=periodo - 1)
                for rs in qs:
                    anterior = round(x['resultado'] - rs['resultado'], 0)
            else:
                anterior = 0
            perspectivas = Perspectiva.objects.all().filter(
                id=x['indicador_id']
            )
            for i in perspectivas:
                total += x['resultado'] * i.peso
        semaforo = Semaforo.objects.values(
            'color__hexadecimal', 'desde', 'hasta')
        for x in semaforo:
            if total >= x['desde'] and total <= x['hasta']:
                context['total'] = {
                    'total': str(total),
                    'color': x['color__hexadecimal']
                }
        context['unidades'] = Unidad.objects.all()
        context['ciclos'] = Ciclo.objects.all().order_by('-id')
        context['semaforo'] = Semaforo.objects.values(
            'desde', 'hasta', 'color__hexadecimal'
        )
        return context


def carga_objetivos(request):
    if request.is_ajax():
        semaforo = Semaforo.objects.values(
            'desde', 'hasta', 'color__hexadecimal'
        )
        context = []
        color = ''
        data = TotalIndicador.objects.values(
            'indicador__objetivo__descripcion',
            'indicador__objetivo_id'
        ).filter(
            indicador__objetivo__perspectiva_id=request.POST['id'],
            periodo_id=request.POST['periodo_id']
        ).annotate(
            Avg('cumplimiento')
        ).order_by(
            'indicador__objetivo_id'
        )
        for x in data:
            res = x['cumplimiento__avg']
            for i in semaforo:
                if (res >= i['desde'] and
                        res <= i['hasta']):
                    color = i['color__hexadecimal']
            context.append({
                'color': color,
                'descripcion': x['indicador__objetivo__descripcion'],
                'resultado': res,
                'id': x['indicador__objetivo_id']
            })
        json_data = json.dumps({'response': context})
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def carga_apertura_indicador(request):
    if request.is_ajax():
        context = []
        context_indicadores = []
        color = ''
        responsable = ''
        semaforo = Semaforo.objects.values(
            'desde',
            'hasta',
            'color__hexadecimal'
        )
        data = Proyecto.objects.values(
            'unidad__descripcion',
            'lider__first_name',
            'lider__last_name',
            'nombre',
            'unidad_id',
            'id'
        ).filter(
            objetivo_id=request.POST['id']
        ).order_by(
            'unidad_id'
        )
        for x in data:
            if KPI.objects.all().filter(proyecto_id=x['id']).exists():
                kpi = KPI.objects.values(
                    'descripcion', 'meta', 'status__descripcion', 'evaluacion'
                ).filter(
                    proyecto_id=x['id']
                )
                for i in kpi:
                    escala = Escala.objects.values(
                        'nombre', 'color__hexadecimal'
                    ).filter(
                        desde__lte=i['evaluacion'],
                        hasta__gte=i['evaluacion']
                    )
                    for esc in escala:
                        context.append({
                            'unidad': x['unidad__descripcion'],
                            'lider_nombre': x['lider__first_name'],
                            'lider_apellido': x['lider__last_name'],
                            'nombre': x['nombre'],
                            'unidad_id': x['unidad_id'],
                            'kpi': i['descripcion'],
                            'meta': i['meta'],
                            'status': i['status__descripcion'],
                            'evaluacion': i['evaluacion'],
                            'escala_nombre': esc['nombre'],
                            'escala_color': esc['color__hexadecimal'],
                            'id': x['id']
                        })
            else:
                context.append({
                    'unidad': x['unidad__descripcion'],
                    'lider_nombre': x['lider__first_name'],
                    'lider_apellido': x['lider__last_name'],
                    'nombre': x['nombre'],
                    'unidad_id': x['unidad_id'],
                    'kpi': '',
                    'meta': '',
                    'status': '',
                    'evaluacion': '',
                    'escala_nombre': '',
                    'escala_color': '',
                    'id': x['id']
                })
        data = TotalIndicador.objects.values(
            'indicador_id',
            'cumplimiento',
            'meta',
            'resultado',
            'indicador__descripcion',
            'indicador__responsable__first_name',
            'indicador__responsable__last_name',
            'indicador__responsable',
        ).filter(
            indicador__objetivo_id=request.POST['id'],
            indicador__activo=True,
            periodo=request.POST['periodo_id']
        )
        if data.count() != 0:
            for x in data:
                for i in semaforo:
                    reslt = x['cumplimiento']
                    if reslt >= i['desde'] and reslt <= i['hasta']:
                        color = i['color__hexadecimal']
                if x['indicador__responsable'] is None:
                    responsable = 'No definido'
                else:
                    responsable = x[
                        'indicador__responsable__first_name'
                    ] + ' ' + x[
                        'indicador__responsable__last_name'
                    ]
                context_indicadores.append({
                    'color': color,
                    'cumplimiento': x['cumplimiento'],
                    'indicador': x['indicador__descripcion'],
                    'responsable': responsable,
                    'id': x['indicador_id'],
                    'meta': x['meta'],
                    'resultado': x['resultado']
                })
        else:
            indicador = TotalIndicador.objects.values(
                'cumplimiento',
                'meta',
                'resultado',
                'indicador_id',
                'indicador__descripcion',
                'indicador__responsable',
                'indicador__responsable__first_name',
                'indicador__responsable__last_name'
            ).filter(
                indicador__objetivo_id=request.POST['id'],
                indicador__activo=True,
                periodo=request.POST['periodo_id']
            )
            for x in indicador:
                if x['indicador__responsable'] is None:
                    responsable = 'No definido'
                else:
                    responsable = x['indicador__responsable__first_name']
                    + ' ' + x['indicador__responsable__last_name']
                context_indicadores.append({
                    'cumplimiento': x['cumplimiento'],
                    'indicador': x['indicador__descripcion'],
                    'responsable': responsable,
                    'id': x['indicador_id'],
                    'meta': x['meta'],
                    'resultado': x['resultado']
                })
        json_data = json.dumps({
            'response': context,
            'response_indicadores': context_indicadores
        })
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def semaforo(request):
    if request.is_ajax():
        context = []
        semaforo = Semaforo.objects.values(
            'desde',
            'hasta',
            'color__hexadecimal'
        )
        for x in semaforo:
            context.append({
                'desde': x['desde'],
                'hasta': x['hasta'],
                'color': x['color__hexadecimal']
            })
        json_data = json.dumps({'response': context})
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def total_dimension(request):
    if request.is_ajax():
        context = []
        cumplimiento = TotalDimension.objects.values(
            'resultado'
        ).filter(
            indicador_id=request.POST['id'],
            periodo_id=request.POST['periodo_id']
        )
        for x in cumplimiento:
            context.append({
                'resultado': x['resultado']
            })
        json_data = json.dumps({'response': context})
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def carga_aperturas_por_indicador(request):
    if request.is_ajax():
        context = []
        sum = 0
        data = ResultadoIndicador.objects.values(
            'indicador__apertura',
            'meta',
            'resultado'
        ).filter(
            indicador__indicador__id=request.POST['id'],
            periodo=request.POST['periodo_id']
        )
        if data.count() != 0:
            for x in data:
                if x['meta'] != 0:
                    semaforo = Semaforo.objects.values(
                        'desde',
                        'hasta',
                        'color__hexadecimal'
                    )
                    for i in semaforo:
                        reslt = round((x['resultado'] / x['meta']) * 100, 0)
                        if reslt >= i['desde'] and reslt <= i['hasta']:
                            color = i['color__hexadecimal']
                    cumpl = round((x['resultado'] / x['meta']) * 100, 0)
                    sum += cumpl
                context.append({
                    'apertura': x['indicador__apertura'],
                    'color': color,
                    'cumplimiento': cumpl
                })
        json_data = json.dumps({
            'response': context
        })
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def tendencia_indicador(request):
    if request.is_ajax():
        context = []
        data = TotalIndicador.objects.values(
            'periodo__descripcion', 'cumplimiento'
        ).filter(
            indicador_id=request.POST[
                'id'], periodo_id__lte=request.POST['periodo_id']
        ).order_by(
            'periodo_id'
        )
        for x in data:
            context.append({
                'periodo': x['periodo__descripcion'],
                'cumplimiento': x['cumplimiento']
            })
        json_data = json.dumps({
            'response': context
        })
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def evolutivo_ciclos(request):
    if request.is_ajax():
        context = []
        observaciones = []
        ciclos = Revision.objects.values(
            'ciclo__ciclo',
            'avance'
        ).filter(proyecto_id=request.POST['id'])
        for x in ciclos:
            ciclo = 'Ciclo: %s' % (x['ciclo__ciclo'])
            context.append({
                'ciclo': ciclo,
                'avance': x['avance'],
                'id': request.POST['id']
            })
        obs = Revision.objects.values(
            'observacion',
            'ciclo__ciclo'
        ).filter(proyecto_id=request.POST['id']).order_by('-id')
        for x in obs:
            ciclo = 'Ciclo: %s' % (x['ciclo__ciclo'])
            observaciones.append({
                'ciclo': ciclo,
                'observacion': x['observacion']
            })
        json_data = json.dumps(
            {'response': context, 'response_obs': observaciones})
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def totales_ciclos(request):
    context = []
    ciclos = TotalCicloUnidad.objects.values(
        'unidad__descripcion',
        'avance'
    ).filter(ciclo_id=request.POST['id']).order_by('-avance')
    semaforo = Semaforo.objects.values(
        'desde',
        'hasta',
        'color__hexadecimal'
    )
    for x in ciclos:
        for i in semaforo:
            reslt = round(x['avance'], 0)
            if (reslt >= i['desde'] and reslt <= i['hasta']):
                color = i['color__hexadecimal']
        context.append({
            'unidad': x['unidad__descripcion'],
            'avance': x['avance'],
            'color': color
        })
    json_data = json.dumps({'response': context})
    return HttpResponse(json_data,
                        content_type='application/json')


def prueba(request):
    pass
