function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(".calugas").on('click', function(){
	var $id = $(this).data('id');
	var $element = $(".objetivos .lista_objetivos");
	var $objetivo = $(this).children('h4').text();
	$(".panel-objetivos > .panel > .panel-heading").html($objetivo);
	$.ajax({
		'method': 'POST',
		'url': 'carga_objetivos/',
		'data': {
			'id': $id,
			'periodo_id': $("#id_periodo").val()
		},
		'success': function(data){
			$(".panel-objetivos").hide().toggle();
			$(".panel-indicadores").hide();
			var count = 1;
			$element.empty();
			if (Object.keys(data.response).length > 0) {
				$.each(data.response, function(key, val){
					$element.append('<div class="row-objetivo" data-id="' + val.id + '" data-resultado="' + val.resultado + '"><span>' + count + '.- ' + val.descripcion + '</span><div class="flex-column"><div class="progress"><div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="' + val.resultado + '" aria-valuemin="0" aria-valuemax="100" style="width: ' + val.resultado + '%; background-color:' + val.color + ';"></div></div><div class="percent-objetivos">' + val.resultado + '%</div></div></div>');
					count += 1;
				});
				creacion_objetivo($id);
			}else{
				$(".panel-objetivos").hide();
			}
			$('html, body').animate({scrollTop:$(document).height()}, 'slow');
			$(".row-objetivo").on('click', function(){
				var $text = $(this).children('span').text();
				var $resultado = $(this).data('resultado');
				$(".panel-indicadores").hide();
				$(".panel-indicadores > .panel > .panel-heading").html('<div>' + $text + '</div><div></div>');
				$.ajax({
					'method': 'POST',
					'url': 'carga_apertura_indicador/',
					'data': {
						'id': $(this).data('id'),
						'periodo_id': $("#id_periodo").val()
					},
					'success': function(data){
						var $contenedor_indicadores = $("#contenedor_indicadores");
						$contenedor_indicadores.empty();
						$.each(data.response_indicadores, function(key, val){
							$contenedor_indicadores.append(
								'<div data-indicador="' + val.id + '" style="display: flex; position: relative; align-items:stretch;"> \
									<div style="align-self: center; min-width: 60%;"> \
										<h6>Indicador: <span id="indicador_objetivo">' + val.indicador + '</span></h6> \
										<h6>Responsable: <span id="responsable_objetivo">' + val.responsable + '</span></h6> \
									</div> \
									<div class="contenedor_graph-indicador" style="border: solid 0.5px ' + val.color + '"> \
										<div style="display: flex;"> \
											<div class="cumplimiento_indicador" style="background-color: ' + val.color + ';"> \
												<h8 style="display: block;">Cumplimiento</h8> \
												<span>' + val.cumplimiento + '%</span> \
											</div> \
										</div> \
										<div class="horizontal_divider"> \
											<div> \
												<h9 style="border-bottom: solid 0.5px ' + val.color + '; background-color: ' + val.color +';">Meta</h9> \
												<span>' + val.meta + '</span> \
											</div> \
											<div> \
												<h9 style="border-bottom: solid 0.5px ' + val.color + '; background-color: ' + val.color +';">Resultado</h9> \
												<span>' + val.resultado + '</span> \
											</div> \
										</div> \
									</div> \
									<div class="tooltip left" id="tooltip-chart-' + val.id + '"> \
										<div class="tooltip-arrow"></div> \
										<div id="tendencia-indicador-' + val.id + '" style="width: 400px; height: 90px; margin-left: 20px;"></div> \
									</div> \
								</div> \
								<div class="aperturas-indicadores" id="apertura-' + val.id + '" style="display: none;"></div>'
							);
							crear_tendencia(val.id);
						});
						var cuenta_obj = 0;
						var proyecto = '';
						
						if (data.response.length == 0) {
							$("[id^=tbody-tab-]").empty();
						}else{
							$.each(data.response, function(key, val){
								var $tbody = '#tbody-tab-' + val.unidad_id;
								if (cuenta_obj == 0) {
									$($tbody).empty();
									if (proyecto == val.nombre) {
										$($tbody).append('<tr><td></td><td data-id="' + val.id + '"></td><td>' + val.kpi + '</td><td>' + val.meta + '</td><td>' + val.status + '</td><td>' + val.evaluacion + '</td><td><small style="background-color:' + val.escala_color + '">' + val.escala_nombre + '</small></td></tr>')
									}else{
										$($tbody).append('<tr><td>' + val.lider_nombre + ' ' + val.lider_apellido + '</td><td data-id="' + val.id + '">' + val.nombre + '</td><td>' + val.kpi + '</td><td>' + val.meta + '</td><td>' + val.status + '</td><td>' + val.evaluacion + '</td><td><small style="background-color:' + val.escala_color + '">' + val.escala_nombre + '</small></td></tr>')
									}
								}else{
									if (proyecto == val.nombre) {
										$($tbody).append('<tr><td></td><td data-id="' + val.id + '"></td><td>' + val.kpi + '</td><td>' + val.meta + '</td><td>' + val.status + '</td><td>' + val.evaluacion + '</td><td><small style="background-color:' + val.escala_color + '">' + val.escala_nombre + '</small></td></tr>')
									}else{
										$($tbody).append('<tr><td>' + val.lider_nombre + ' ' + val.lider_apellido + '</td><td data-id="' + val.id + '">' + val.nombre + '</td><td>' + val.kpi + '</td><td>' + val.meta + '</td><td>' + val.status + '</td><td>' + val.evaluacion + '</td><td><small style="background-color:' + val.escala_color + '">' + val.escala_nombre + '</small></td></tr>')
									}
								}
								cuenta_obj += 1;
								proyecto = val.nombre;
							});
						}
						$("#contenedor_indicadores > div").on('click', function(){
							var $id_click = $(this).data('indicador');
							$.ajax({
								'method': 'POST',
								'url': 'carga_aperturas_por_indicador/',
								'data': {
									'id': $id_click,
									'periodo_id': $("#id_periodo").val()
								},
								'success': function(data){
									$("#apertura-" + $id_click).empty();
									if (Object.keys(data.response).length > 0) {
										$.each(data.response, function(key, val){
											if (typeof val.apertura != 'undefined') {
												$("#apertura-" + $id_click).append('<div class="apertura_objetivo" style="border-top: 10px solid ' + val.color + '; border-color: ' + val.color + ';"><span>' + val.cumplimiento + '%</span>' + val.apertura + '</div>');
											}
										});
										$("#apertura-" + $id_click).slideToggle();
									}
								}
							});
						});
						$(".panel-indicadores").slideToggle();
						$('html, body').animate({scrollTop:$(document).height()}, 'slow');
					}
				});
			});
		}
	});
});

function creacion_objetivo(id){
	var tick = [];
	$.get('semaforo/', function(data, status){
		$.each(data.response, function(key, val){
			tick.push(val.hasta);
		});
	});
	$('#graph-objetivo').highcharts({
	        chart: {
	            type: 'gauge',
	            margin: 10,
	            backgroundColor: 'transparent'
	        },

	        title: null,

	        pane: {
	            center: ['50%', '85%'],
	            size: '120%',
	            startAngle: -90,
	            endAngle: 90,
	            background: null
	        },

	        tooltip: {
	            enabled: false
	        },
	        
	        yAxis: {
	            tickPositions: tick,
	            tickmarkPlacement: 'on',
	            tickLength: 54,
	            minorTickLength: 1,
	            min: 0,
	            max: 100,
	            labels: {
	              distance: 20,
	              format: '{value}%'
	            }        
	        },

	        plotOptions: {
	            gauge: {
	              dataLabels: {
	                enabled: false
	              },
	              dial: {
	                baseLength: '0%',
	                baseWidth: 10,
	                radius: '100%',
	                rearLength: '0%',
	                topWidth: 1
	              }
	            }
	        },

	        credits: {
	            enabled: false
	        },

	        series: [{
	            name: 'Speed',
	            data: [0]
	        }]
	});

	$.get('semaforo/', function(data, status){
		var chart = $('#graph-objetivo').highcharts();
		$.each(data.response, function(key, val){
			chart.yAxis[0].addPlotBand({
				from: val.desde,
	          	to: val.hasta,
	          	color: val.color,
	          	thickness: '50%'
			});
		});
	});

	var valor_response = 0;

	$.ajax({
    	'method': 'POST',
		'url': 'totaldimension/',
		'data': {
			'id': id,
			'periodo_id': $("#id_periodo").val()
		},
		'success': function(data){
			$.each(data.response, function(key, val){
    			valor_response = val.resultado;
    			$('#graph-objetivo').siblings('span').empty();
    			$('#graph-objetivo').siblings('span').text(val.resultado + '%');
			});
		}
    });

	setTimeout(function () {

	    var chart = $('#graph-objetivo').highcharts(),
	        point,
	        newVal,
	        inc;

	    valor = valor_response;

	    if (chart) {
	        point = chart.series[0].points[0];
	        newVal = point.y + parseFloat(valor);

	        point.update(newVal);
	    }
	}, 1000);
}

var total = $("#yourcircle").data('value');
var color = $("#yourcircle").data('color');

$("#yourcircle").circliful({
	backgroundBorderWidth: 10,
	fillColor: 'white',
	fontColor: color,
	foregroundBorderWidth: 5,
	foregroundColor: color,
	percent: total,
	text: 'cumplimiento',
	textStyle: 'font-size: 0.7em;'
});

$(".circliful text").attr('y', '100');
$(".circliful text:first-child").attr('y', '115');

$(".circliful text:first-child").insertAfter(".circliful .timer");


function crear_tendencia($id){

	$.ajax({
		'method': 'POST',
		'url': 'tendencia_indicador/',
		'data': {
			'id': $id,
			'periodo_id': $("#id_periodo").val()
		},
		'success': function(data){
			if (Object.keys(data.response).length > 1) {
				var periodos = []
				var cumplimientos = []
				$("#tendencia-indicador-" + $id).highcharts({
					chart: {
						type: 'area',
						borderColor: '#CCC',
						borderWidth: 0.5
					},
					title: null,
					xAxis: {
						labels: {
							enabled: false
						}
					},
					yAxis: {
						title: null,
						max: 100,
						min: 0,
						tickInterval: 20,
						gridLineWidth: 0
					},
					tooltip: {
						valueSuffix: ' %'
					},
					credits: {
						enabled: false
					},
					legend: {
			            enabled: false
			        },
			        plotOptions: {
			            area: {
			            	lineColor: '#00669E',
			            	fillOpacity: 0.5,
			            	marker: {
			            		fillColor: '#00669E'
			            	}
			            }
			        }
				});

				$.each(data.response, function(key, val){
					periodos.push(val.periodo);
					cumplimientos.push(val.cumplimiento);
				});

				var chart_finish = $("#tendencia-indicador-" + $id).highcharts();

				chart_finish.xAxis[0].setCategories(periodos);
				var series = {data: cumplimientos, name: 'Cumplimiento'};
				chart_finish.addSeries(series);
			}
		}
    });
}


$("tbody").on('click', 'tr', function(e){
	var $element = $(this);
	var $id = $(this).children('td:nth-child(2)').data('id');
	$.ajax({
		'method': 'POST',
		'url': 'evolutivo_ciclos/',
		'data': {
			'id': $id
		},
		'success': function(data){
			$(".tr_data").remove();
			if (Object.keys(data.response).length > 1) {
				var periodos = []
				var cumplimientos = []
				var observaciones = []
				if ($element.children('td:nth-child(2)').text() != ""){
					$.each(data.response, function(key, val){
						$('<tr class="tr_data" id="detalle_proyecto_' + val.id + '"> \
								<td colspan="7"> \
									<div> \
										<div> \
											<div id="evolutivo_ciclo_proy_' + $id + '" style="height: 200px;"></div> \
										</div> \
										<div> \
											<div class="timeline" id="timeline_' + val.id + '"></div> \
										</div> \
									</div>\
								</td> \
						</tr>').insertAfter($element);
						return false;
					});
					$.each(data.response, function(key, val){
						periodos.push(val.ciclo);
						cumplimientos.push(val.avance);
					});
					$.each(data.response_obs, function(key, val){
						$("#timeline_" + $id).append('<div> \
							<span>Observación ' + val.ciclo + '</span> \
							<p>' + val.observacion + '</p> \
						</div>');
					});
					$("#evolutivo_ciclo_proy_" + $id).highcharts({
						chart: {
							type: 'area',
							borderColor: '#CCC',
							borderWidth: 0.5,
							marginTop: 30
						},
						title: null,
						xAxis: {
							labels: {
								enabled: true
							}
						},
						yAxis: {
							title: null,
							max: 100,
							min: 0,
							tickInterval: 20,
							gridLineWidth: 0
						},
						tooltip: {
							valueSuffix: ' %'
						},
						credits: {
							enabled: false
						},
						legend: {
				            enabled: false
				        },
				        plotOptions: {
				            area: {
				            	lineColor: '#00669E',
				            	fillOpacity: 0.5,
				            	marker: {
				            		fillColor: '#00669E'
				            	}
				            }
				        }
					});

					var chart_finish = $("#evolutivo_ciclo_proy_" + $id).highcharts();

					chart_finish.xAxis[0].setCategories(periodos);
					var series = {data: cumplimientos, name: 'Cumplimiento'};
					chart_finish.addSeries(series);

				}	
			}else{
				swal({
					title: 'Falta Información',
					text: 'No existen datos cargados para este proyecto',
					type: 'warning'
				});
			}
		}
	});
});

$("#ciclos").change(function(){
	var option = $(this).find('option:selected').val();
	var ciclo = $(this).find('option:selected').text();
	$("#myModalGraph").highcharts({
		chart: {
			type: 'bar'
		},
		title: {
			text: 'Avance ' + ciclo
		},
		subtitle: {
			text: 'Porcentaje de avance considerando todas las prioridades codificadas por Unidad, incluyendo BSC Unidades'
		},
		credits: {
			enabled: false
		},
		plotOptions: {
			bar: {
				dataLabels: {
					enabled: true,
					format: '{y} %',
					style: {
						fontWeight: 'bold',
						fontSize: '16px'
					}
				}
			},
			series: {
				color: '#FE9C48'
			}
		},
		legend: {
			enabled: false
		},
		yAxis: {
			gridLineWidth: 0,
			title: {
				text: null
			},
			labels: {
				format: '{value}%'
			}
		}
	});

	$.ajax({
		'method': 'POST',
		'url': 'totales_ciclos/',
		'data': {
			'id': option
		},
		'success': function(data){
			var unidades = [];
			var avances = [];
			if (Object.keys(data.response).length > 1) {
				$.each(data.response, function(key, val){
					unidades.push(val.unidad);
					avances.push({
						y: val.avance
					});
				});

				var chart_finish = $("#myModalGraph").highcharts();

				chart_finish.xAxis[0].setCategories(unidades);
				var series = {data: avances, name: '% Avance'};
				chart_finish.addSeries(series);

				$("#myModal").modal({
					show: true
				});

			}else{
				swal({
					title: 'Falta Información',
					text: 'No existen datos cargados para este proyecto',
					type: 'warning'
				});
			}
		}
	});
});

