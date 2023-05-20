$(document).ready(function() {
    function updateImages() {
        // For each img tag with a 'card-img-top' class
        $('img.card-img-top').each(function() {
            var img = $(this);
            var livestream_id = img.attr('data-id');
            fetchImage(livestream_id, img); // Pass img to fetchImage
        });
    }

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

    // Update the images immediately
    updateImages();

    // Then update every 60 seconds
    setInterval(updateImages, 60000);
});
