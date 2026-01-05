document.addEventListener('DOMContentLoaded', function() {
    var mapElement = document.getElementById('map');
    if (!mapElement) return;

    var defaultCenter = [25.0330, 121.5654];
    var map = L.map('map').setView(defaultCenter, 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var hasUserLocation = false;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            hasUserLocation = true;
            var latlng = [pos.coords.latitude, pos.coords.longitude];
            map.setView(latlng, 13);
            var label = window.userLocationLabel || 'You are here';
            L.marker(latlng).addTo(map).bindPopup('<b>' + label + '</b>').openPopup();
        });
    }

    if (typeof shopData !== 'undefined') {
        shopData.forEach(function(shop) {
            if (!shop.lat || !shop.lng) return;
            var marker = L.marker([shop.lat, shop.lng]).addTo(map);
            marker.bindPopup('<b>' + shop.name + '</b><br>' + shop.address + '<br>剩餘: ' + shop.food_count + ' 份');
        });

        // 若沒有定位，用第一個商家當中心
        if (!hasUserLocation && shopData.length && shopData[0].lat && shopData[0].lng) {
            map.setView([shopData[0].lat, shopData[0].lng], 13);
        }
    }
});
