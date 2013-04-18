/*
 * Released under the MIT license
 */

function _ajax_request(url, data, callback, method) {
    return jQuery.ajax({
        url: url,
        type: method,
        data: data,
        success: callback
    });
}

jQuery.extend({
    post: function(url, data, callback) {
        return _ajax_request(url, data, callback, 'POST');
}});

(function() {
    var cameraCanvas = document.getElementById("cam");
    var capturing = false;
    var overlay = new Image();
    overlay.src = "/static/overlay.png";

    DEBUG = document.getElementById("debug");

    var rgbToHex = function(r, g, b) {
        if(r < 0 || r > 255) alert("r is out of bounds; "+r);
        if(g < 0 || g > 255) alert("g is out of bounds; "+g);
        if(b < 0 || b > 255) alert("b is out of bounds; "+b);
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1,7);
    };

    var mirrorCanvas = function(canvas){
        var ctx = canvas.getContext("2d");
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
    };

    var drawOverlay = function(canvas, overlay){
        var ctx = canvas.getContext("2d");
        mirrorCanvas(cameraCanvas);
        ctx.drawImage(overlay, 0, 0);
        mirrorCanvas(cameraCanvas);
    };

    var resultCallback = function(result) {
        colors = result['colors'];
        // Display colors
        var hexColor1 = rgbToHex(colors[0], colors[1], colors[2]);
        var hexColor2 = rgbToHex(colors[3], colors[4], colors[5]);
        $('#box1').css('background-color', hexColor1);
        $('#box2').css('background-color', hexColor2);

        // DEBUG.innerHTML = hexColor1 + ' | ' + hexColor2;
    };

    camera.init({
        fps: 30,
        mirror: true,
        targetCanvas: cameraCanvas,

        onFrame: function(canvas) {
            var ctx = cameraCanvas.getContext("2d");

            // DEBUG.innerHTML = cameraCanvas.width + 'x' + cameraCanvas.height;

            drawOverlay(cameraCanvas, overlay);
        },

        onSuccess: function() {
            var shootBtn = document.getElementById("shoot");
            var sendBtn = document.getElementById("send");
            var retryBtn = document.getElementById("retry");

            document.getElementById("info").style.display = "none";

            capturing = true;
            document.getElementById("buttons").style.display = "block";
            shootBtn.onclick = function() {
                shootBtn.style.display = "none";
                sendBtn.style.display = "inline";
                retryBtn.style.display = "inline";

                camera.pause();
                capturing = !capturing;
            };

            retryBtn.onclick = function() {
                shootBtn.style.display = "block";
                sendBtn.style.display = "none";
                retryBtn.style.display = "none";

                camera.start();
                capturing = !capturing;
            };

            sendBtn.onclick = function() {
                sendBtn.disabled = true;
                retryBtn.disabled = true;

                // Fully blind the spare part of the picture
                drawOverlay(cameraCanvas, overlay);
                drawOverlay(cameraCanvas, overlay);
                drawOverlay(cameraCanvas, overlay);
                drawOverlay(cameraCanvas, overlay);

                // TODO: Show some 'waiting' animation

                // Send data to server
                $.post('colors',
                        {
                            img : cameraCanvas.toDataURL('image/jpeg')
                        },
                        resultCallback);
            };
        },

        onError: function(error) {
            // TODO: log error
        },

        onNotSupported: function() {
            document.getElementById("info").style.display = "none";
            cameraCanvas.style.display = "none";
            document.getElementById("notSupported").style.display = "block";
        }
    });
})();