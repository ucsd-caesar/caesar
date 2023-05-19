window.onload = function() {
    for (var livestreamId in hlsLinks) {
        var video = document.getElementById('video-' + livestreamId);
        var videoSrc = hlsLinks[livestreamId];
        if(Hls.isSupported()) {
            var hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {
                video.play();
            });
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = videoSrc;
            video.addEventListener('loadedmetadata', function() {
                video.play();
            });
        }
    }
}
