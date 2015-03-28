var map = null;
var lat = 40.769723;
var lng = -73.963051;
var randomMultiplier = 20;
var markersArr = [];

function initialize(param) {

    

    var map_canvas = document.getElementById('googleMap');

    var map_options = {
        center: new google.maps.LatLng(lat, lng),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scrollwheel: false
    };

    map = new google.maps.Map(map_canvas, map_options);

    var styles = [
        {
            "featureType": "landscape",
            "stylers": [
                { "visibility": "on" }

            ]
        },{
            "featureType": "poi",
            "stylers": [
                { "visibility": "off" }
            ]
        },{
            "featureType": "road",
            "stylers": [

            ]
        },{
            "elementType": "geometry.stroke",
            "stylers": [
                { "visibility": "off" }
            ]
        },{
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                { "visibility": "on" }

            ]
        },{
            "featureType": "landscape",
            "elementType": "labels.text.stroke",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "poi",
            "elementType": "labels.icon",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                { "visibility": "off" }

            ]
        },{
            "featureType": "water",
            "elementType": "labels.text.stroke",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "water",

        },{
        }
    ]
    map.setOptions({styles: styles});


    if (!param){

	for (var i = 0; i < 5; i++) {
            var randomAddonLat = (Math.random() - 0.5) / 80;
            var randomAddonLng = (Math.random() - 0.5) / 80;
            laglng = new google.maps.LatLng(lat + randomAddonLat, lng + randomAddonLng);
            var marker = addStaticMarker(laglng, "Aashir");
            markersArr.push(marker);
	};
	
	
    };
}

function addStaticMarker(laglng, name){

    if (!laglng) {
        laglng = map.getCenter();
    }
    var marker = new google.maps.Marker({
        position: laglng,
        map: map,
        animation: google.maps.Animation.DROP,
        icon: "static/ParkSwap/images/markerPrice2.gif"
    });

    var content = '<p>' + name + ' has a free spot here in ' + Math.floor(Math.random() * 10) + ' minute(s).</p>' +
    '<div style="text-align:center"><form action="/accepted-parking" method="GET"><button class="btn btn-inverse btn-sm" type="submit">Confirm</button></form></div>'
    //'<div style="text-align:center"><a href='+' "/accepted-parking" '+  ">Confirm</a></div>";


    var iw = new google.maps.InfoWindow({
       content: content
    });
    google.maps.event.addListener(marker, "click", function (e) {
        iw.open(map, marker);
    });

    return marker;
}


function addMarker(laglng, name){
    if (!laglng) {
        laglng = map.getCenter();
    }
    var marker = new google.maps.Marker({
        position: laglng,
        map: map
    });

    var iw = new google.maps.InfoWindow({

	   content: (name + " has a free spot here in " + Math.floor(Math.random() * 10) + " minute(s).")
    });
    google.maps.event.addListener(marker, "click", function (e) { iw.open(map, this); });


}

function addCarMarker(laglng, name){
    if (!laglng) {
        laglng = map.getCenter();
    }
    var marker = new google.maps.Marker({
        position: laglng,
        map: map,
        animation: google.maps.Animation.DROP,
        icon: "static/ParkSwap/images/car.png"
    });

    var iw = new google.maps.InfoWindow({

       content: (name + " will arrive in " + Math.floor(Math.random() * 10) + " minute(s).")
    });
    google.maps.event.addListener(marker, "click", function (e) { iw.open(map, this); });


}


function initializeAccepted() {
    var map_canvas = document.getElementById('googleMap');

    var map_options = {
        center: new google.maps.LatLng(lat, lng),
        zoom: 16,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scrollwheel: false
    };

    map = new google.maps.Map(map_canvas, map_options);

    var styles = [
        {
            "featureType": "landscape",
            "stylers": [
                { "visibility": "on" }

            ]
        },{
            "featureType": "poi",
            "stylers": [
                { "visibility": "off" }
            ]
        },{
            "featureType": "road",
            "stylers": [

            ]
        },{
            "elementType": "geometry.stroke",
            "stylers": [
                { "visibility": "off" }
            ]
        },{
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                { "visibility": "on" }

            ]
        },{
            "featureType": "landscape",
            "elementType": "labels.text.stroke",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "poi",
            "elementType": "labels.icon",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                { "visibility": "off" }

            ]
        },{
            "featureType": "water",
            "elementType": "labels.text.stroke",
            "stylers": [
                { "visibility": "on" }
            ]
        },{
            "featureType": "water",

        },{
        }
    ]
    map.setOptions({styles: styles});

    var randomAddonLat = (Math.random() - 0.5) / 80;
    var randomAddonLng = (Math.random() - 0.5) / 80;

    var laglng1 = new google.maps.LatLng(lat + randomAddonLat, lng + randomAddonLng);
    addMarker(laglng1, "Aashir");

    var laglng2 = new google.maps.LatLng(lat, lng);
    addCarMarker(laglng2, "Aashir");

    var path = new google.maps.MVCArray();

    //Intialize the Direction Service
    var service = new google.maps.DirectionsService();

    //Set the Path Stroke Color
    var poly = new google.maps.Polyline({
      map: map,
      strokeWeight: 6,
      strokeColor: '#4986E7'
    });

    var src = laglng1;
    var des = laglng2;
    // path.push(src);
    poly.setPath(path);
    service.route({
      origin: src,
      destination: des,
      travelMode: google.maps.DirectionsTravelMode.DRIVING
    }, function(result, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        for (var i = 0, len = result.routes[0].overview_path.length; i < len; i++) {
          path.push(result.routes[0].overview_path[i]);
        }
      }
    });


    var content = "hello world";
    var iw = new google.maps.InfoWindow({
       content: content
    });
    google.maps.event.addListener(marker, "click", function (e) {
        iw.open(map, marker);
    });
}

/*
$(document).ready(function () {

/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/* google */
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
var map_canvas = document.getElementById('googleMap');

var map_options = {
    center: new google.maps.LatLng(44.434596, 26.080533),
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scrollwheel: false
};

var map = new google.maps.Map(map_canvas, map_options);




google.maps.event.addDomListener(window, 'load', initialize);


});
*/
