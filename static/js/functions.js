function initialize() {
	var display = true
	var latlng = new google.maps.LatLng(-3.06526732445,37.3584060669);
	var myOptions = {
		zoom: 12,
		center: latlng,
		draggable: false,
		disableDoubleClickZoom: true,
		scrollwheel: false,
		mapTypeControl: false,
		keyboardShortcuts: false,
		navigationControl: false,
		mapTypeId: google.maps.MapTypeId.SATELLITE
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
	$.each(locations, function(intIndex, location) {
		var latlng = new google.maps.LatLng(location.lat , location.lng);
		if (location.note != false && display== true) {
		var infowindow = new google.maps.InfoWindow({
      			position: latlng, 
    			content: location.note
		});
		infowindow.open(map);
		display = false
		}
		var marker = new google.maps.Marker({
      		position: latlng, 
      		map: map, 
  		}); 	
	});
}


function showImage(id) {
	$("#image").removeClass('invisible');
	$("#imagediv").load("/image/" + id);
}


function showAudio(id) {
	$("#audio").removeClass('invisible');
	$("#audiodiv").load("/audio/" + id);
}


function hideImage() {
	$("#imagediv").html("");
	hideAllContentWindows();
}

function showContentWindow(name) {
	$('#'+ name).removeClass('invisible');
}


function hideAllContentWindows() {
	$('.content').addClass('invisible');
}
