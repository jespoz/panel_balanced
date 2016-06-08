from django.conf.urls import url
from .views import IndexView
from . import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^carga_objetivos/$', views.carga_objetivos),
    url(r'^carga_apertura_indicador/$', views.carga_apertura_indicador),
    url(r'^carga_aperturas_por_indicador/$',
        views.carga_aperturas_por_indicador),
    url(r'^semaforo/$', views.semaforo),
    url(r'^totaldimension/$', views.total_dimension),
    url(r'^tendencia_indicador/$',
        views.tendencia_indicador),
    url(r'^evolutivo_ciclos/', views.evolutivo_ciclos),
    url(r'^totales_ciclos/', views.totales_ciclos),

    url(r'^prueba/$', views.prueba),
]
