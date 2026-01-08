document.addEventListener('DOMContentLoaded', function() {
    var mapElement = document.getElementById('map');
    var shopCards = document.querySelectorAll('.shop-card');
    var locateButtons = document.querySelectorAll('.btn-locate');
    var markersById = {};
    var mapInstance = null;
    var userMarker = null;
    var userCoords = null;
    var fillLocationBtn = document.getElementById('btn-fill-location');
    var latInput = document.querySelector('input[name="latitude"]');
    var lngInput = document.querySelector('input[name="longitude"]');

    function addBadge(card, type, text) {
        var container = card.querySelector('.shop-badges');
        if (!container || container.querySelector('[data-badge="' + type + '"]')) {
            return;
        }
        var span = document.createElement('span');
        span.className = type === 'most' ? 'badge bg-warning text-dark ms-1' : 'badge bg-primary ms-1';
        span.dataset.badge = type;
        span.textContent = text;
        container.appendChild(span);
        if (type === 'most') {
            card.dataset.most = 'true';
        } else if (type === 'nearest') {
            card.dataset.nearest = 'true';
        }
    }

    function clearBadge(card, type) {
        var container = card.querySelector('.shop-badges');
        if (!container) return;
        container.querySelectorAll('[data-badge="' + type + '"]').forEach(function(el) {
            el.remove();
        });
        if (type === 'most') {
            delete card.dataset.most;
        } else if (type === 'nearest') {
            delete card.dataset.nearest;
        }
    }

    function reorderCards() {
        var container = document.getElementById('nearby-shops');
        if (!container) return;
        var columns = Array.from(container.querySelectorAll('.col-md-4'));
        if (!columns.length) return;

        var ordered = [];
        var mostCard = columns.find(function(card) { return card.querySelector('.shop-card')?.dataset.most === 'true'; });
        if (mostCard) {
            ordered.push(mostCard);
        }

        var nearestCard = columns.find(function(card) {
            var dataset = card.querySelector('.shop-card')?.dataset || {};
            return dataset.nearest === 'true' && ordered.indexOf(card) === -1;
        });
        if (nearestCard) {
            ordered.push(nearestCard);
        }

        var rest = columns.filter(function(card) { return ordered.indexOf(card) === -1; });
        var newOrder = ordered.concat(rest);
        newOrder.forEach(function(card) {
            container.appendChild(card);
        });
        setMarkerIcons();
    }

    function applyMostSupplyBadge() {
        var quantities = Array.from(shopCards).map(function(card) {
            return parseInt(card.dataset.quantity || '0', 10);
        });
        var maxQty = Math.max.apply(null, quantities);
        if (!isFinite(maxQty) || maxQty <= 0) return;
        shopCards.forEach(function(card, idx) {
            clearBadge(card, 'most');
            var qty = parseInt(card.dataset.quantity || '0', 10);
            if (qty === maxQty && badgeLabels && badgeLabels.most) {
                addBadge(card, 'most', badgeLabels.most);
            }
        });
        reorderCards();
        setMarkerIcons();
    }

    function haversine(lat1, lon1, lat2, lon2) {
        function toRad(value) {
            return value * Math.PI / 180;
        }
        var R = 6371; // km
        var dLat = toRad(lat2 - lat1);
        var dLon = toRad(lon2 - lon1);
        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    function applyNearestBadge(userLat, userLng) {
        var nearestCards = [];
        var minDistance = Infinity;
        shopCards.forEach(function(card) {
            clearBadge(card, 'nearest');
            var lat = parseFloat(card.dataset.lat);
            var lng = parseFloat(card.dataset.lng);
            if (isNaN(lat) || isNaN(lng)) return;
            var distance = haversine(userLat, userLng, lat, lng);
            if (distance < minDistance - 0.01) {
                minDistance = distance;
                nearestCards = [card];
            } else if (Math.abs(distance - minDistance) < 0.01) {
                nearestCards.push(card);
            }
        });
        if (!isFinite(minDistance) || minDistance === Infinity) return;
        nearestCards.forEach(function(card) {
            if (badgeLabels && badgeLabels.nearest) {
                addBadge(card, 'nearest', badgeLabels.nearest);
            }
        });
        reorderCards();
        setMarkerIcons();
    }

    // 首頁載入就先標記「物資最多」
    applyMostSupplyBadge();

    // 商家註冊：一鍵填入目前經緯度（無需地圖）
    if (fillLocationBtn && latInput && lngInput) {
        fillLocationBtn.addEventListener('click', function() {
            if (!navigator.geolocation) return;
            navigator.geolocation.getCurrentPosition(function(pos) {
                latInput.value = pos.coords.latitude.toFixed(6);
                lngInput.value = pos.coords.longitude.toFixed(6);
            }, function() {
                var msg = fillLocationBtn.dataset.error || 'Unable to get your location.';
                alert(msg);
            });
        });
    }

    if (!mapElement) {
        return;
    }

    var defaultCenter = [25.0330, 121.5654];
    var map = L.map('map').setView(defaultCenter, 13);
    mapInstance = map;

    function coloredIcon(className) {
        return L.divIcon({
            className: 'custom-marker ' + className,
            iconSize: [18, 18],
            iconAnchor: [9, 9]
        });
    }

    var iconDefault = coloredIcon('marker-default');
    var iconMost = coloredIcon('marker-most');
    var iconNearest = coloredIcon('marker-nearest');
    var iconUser = coloredIcon('marker-user');

    function setMarkerIcons() {
        shopCards.forEach(function(card) {
            var id = card.dataset.id;
            if (!id || !markersById[id]) return;
            var marker = markersById[id];
            if (card.dataset.most === 'true') {
                marker.setIcon(iconMost);
            } else if (card.dataset.nearest === 'true') {
                marker.setIcon(iconNearest);
            } else {
                marker.setIcon(iconDefault);
            }
        });
    }

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var hasUserLocation = false;

    function setUserLocation(lat, lng, zoom) {
        userCoords = [lat, lng];
        var label = window.userLocationLabel || 'You are here';
        if (userMarker) {
            userMarker.setLatLng(userCoords);
        } else {
            userMarker = L.marker(userCoords, { icon: iconUser }).addTo(map).bindPopup('<b>' + label + '</b>');
        }
        map.setView(userCoords, zoom || 13);
        userMarker.openPopup();
        applyNearestBadge(lat, lng);
    }

    function requestUserLocation(forceZoom) {
        if (userCoords) {
            setUserLocation(userCoords[0], userCoords[1], forceZoom ? 16 : 13);
            return;
        }
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                hasUserLocation = true;
                setUserLocation(pos.coords.latitude, pos.coords.longitude, 16);
            }, function() {
                // ignore errors
            });
        }
    }

    // 自動嘗試取得位置
    requestUserLocation(false);

    if (typeof shopData !== 'undefined') {
        shopData.forEach(function(shop) {
            if (!shop.lat || !shop.lng) return;
            var marker = L.marker([shop.lat, shop.lng], { icon: iconDefault }).addTo(map);
            var remainingText = (window.transRemaining || 'Remaining') + ': ' + shop.food_count;
            marker.bindPopup('<b>' + shop.name + '</b><br>' + shop.address + '<br>' + remainingText);
            if (shop.id) {
                markersById[shop.id] = marker;
            }
        });

        // 若沒有定位，用第一個商家當中心
        if (!hasUserLocation && shopData.length && shopData[0].lat && shopData[0].lng) {
            map.setView([shopData[0].lat, shopData[0].lng], 13);
        }
    }
    locateButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var lat = parseFloat(this.dataset.lat);
            var lng = parseFloat(this.dataset.lng);
            if (isNaN(lat) || isNaN(lng) || !mapInstance) return;
            mapInstance.setView([lat, lng], 16);
            var marker = markersById[this.dataset.shopId];
            if (marker) {
                marker.openPopup();
            }
        });
    });

    var myLocationBtn = document.getElementById('btn-my-location');
    if (myLocationBtn) {
        myLocationBtn.addEventListener('click', function() {
            requestUserLocation(true);
        });
    }

    // Initial icon update based on existing badges (e.g., most supply)
    setMarkerIcons();

});
