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
        DEBUG.innerHTML = result['colors'];
        // TODO: Display colors
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