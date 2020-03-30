/**
 * Función para mover elementos de un select múltiple a otro
 * @param sender Recibe un string con el id del objeto que envía
 * @param reciver Recibe un string con el id del objeto que recibe
*/
function move_select_text(sender,reciver){
	var values_list = $(sender).val();
	$.each(values_list,function(key,value){
		if(value!=''){
			$(reciver).append($(sender+ ' option[value='+value+']'));
		}
	});
	get_alloption_selected();
}

/**
 * Función para limpiar valores repetidos en el
 * select de los guardias
*/
function clear_guardias(){
	$.each($('#id_guardias option'),function(key,value){
		if($(value).val()!='')
		{
			$.each($('#id_guardias_list option'),function(key2,value2){
				if($(value).val()==$(value2).val()){
					$(value2).remove();
				}
			});
		}
	});
}

/**
 * Función para marcar las opciones del select de guardias
 * como seleccionadas
*/
function get_alloption_selected(){
	$('#id_guardias option').each(function(key,value){
		$(value).prop('selected',true);
	});
	$('#id_guardias').change();
}

/**
 * Función para mostrar el modal con el mapa
 * @param latitud Recibe la latitud a mostrar
 * @param longitud Recibe la longitud a mostrar
*/
function show_map_modal(latitud,longitud){
	var lat_lang = {lat: parseFloat(latitud), lng: parseFloat(longitud)};
    var map = new google.maps.Map($('.map_modal #map')[0], {
      zoom: 15,
      center: lat_lang
    });
    var marker = new google.maps.Marker({
      position: lat_lang,
      map: map
    });
    map.setCenter(new google.maps.LatLng(parseFloat(latitud),parseFloat(longitud)));
	$('.map_modal').modal();
}

/**
 * Función para mostrar un contenido
 * @param select_val Recibe el valor del select
 * @param value Recibe el valor de comparación
 * @param html Recibe el id/clase del elemento a mostrar
 * @param delay Recibe el retraso de la animacion
*/
function show_content(select_val,value,html,delay=500){
	if(select_val==value){
		$(html).show(delay);
	}
	else{
		$(html).hide(delay);
	}
}

/**
 * Función para cargar el mapa de google
 * @param latitud Recibe la latitud a mostrar
 * @param longitud Recibe la longitud a mostrar
*/
function load_google_map(latitud=0,longitud=0){
	if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
      	set_map(position.coords.latitude,position.coords.longitude);
      }, function() {
        set_map(latitud,longitud);
      });
    } 
    else {
      set_map(latitud,longitud);
    }
}

/**
 * Función para mostrar un contenido
*/
function register_show(value){
	var delay = 500;
	if(value==2){
		$("#servicio").show(delay);
		$("#guardia").show(delay);
	}
	else if(value==3){
		$("#servicio").show(delay);
		$("#guardia").hide(delay);
	}
	else{
		$("#servicio").hide(delay);
		$("#guardia").hide(delay);
	}
}

function set_map(latitud,longitud){
	update_location_form(latitud, longitud);
	var myLatlng = {lat:latitud,lng:longitud}
	var ChiapasLatlng = {lat: 16.3515794,lng: -92.8778331};
	var map = new google.maps.Map($('#map')[0],{
      zoom: 8,
      center: ChiapasLatlng
    //   center: myLatlng
    });
    var marker = new google.maps.Marker({
		position: myLatlng,
	    map: map,
	    draggable:true,
	});
	map.addListener('click', function(e) {
		window.marker = marker;
		marker.setPosition(e.latLng);
		update_location_form(e.latLng.lat(), e.latLng.lng());
	});

}

/** 
 * Función para asignar o actualizar la latitud y longitud
 * del formulario
*/
function update_location_form(lat, long){
	$('#id_latitud_inicial').val(lat);
	$('#id_longitud_inicial').val(long);
}