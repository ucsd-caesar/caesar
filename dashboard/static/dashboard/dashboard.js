// Fetch image from api and update the image source
function fetchImage(livestream_id, img) {
    // Fetch the latest image for this livestream
    var url = '/api/livestreams/' + livestream_id;
    $.getJSON(url, function(data) {
        // Update the image source
        // Append a timestamp to the image URL to bypass cache
        var new_src = data.source + '?' + new Date().getTime();
        img.attr('src', new_src);
    });
}

// Create an observer instance
var observer = new IntersectionObserver(function(entries) { 
    entries.forEach(function(entry) {
        var img = $(entry.target);
        var livestream_id = img.attr('data-id');

        // If the image is in view
        if (entry.isIntersecting) {
            // Fetch image immediately
            fetchImage(livestream_id, img);

            // Then fetch image every 60 seconds
            img.data('intervalId', setInterval(fetchImage, 60000, livestream_id, img));
        } else {
            // If element is out of the viewport, clear the interval
            clearInterval(img.data('intervalId'));
        }
    });
});

$(document).ready(function() {
    $('img.card-img-top').each(function() {
        observer.observe(this);
    });
});
