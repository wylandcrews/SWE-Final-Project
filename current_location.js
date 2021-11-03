function currentLocation() {
    if (navigator.geolocation) {
        starting_position = navigator.geolocation.getCurrentPosition(getPosition);
    }
}

function getPosition(position) {
    position_response = "Latitude: " + position.coords.latitude + ", Longitude: " + position.coords.longitude;
    console.log(position_response);
}