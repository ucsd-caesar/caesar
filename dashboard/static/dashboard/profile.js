
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const stopBtns = document.querySelectorAll('.stop-btn');

function setUserId(id) {
    user_id = id;
}

// add event listener for each stopbtn
stopBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
        const tableRow = btn.parentElement.parentElement;
        const livestreamId = btn.getAttribute('data-stream-id');

        const response = await fetch('{% url "dashboard:stop_stream" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: new URLSearchParams({livestream_id: livestreamId}),
        });

        const result = await response.json();
        if (result.status === 'success') {
            tableRow.remove();
        } else {
            console.error(result.message);
        }
    });
});

// add event listener for each viewport button
const viewportBtns = document.querySelectorAll('.open-viewport-btn');
viewportBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
        const viewport_id = btn.getAttribute('data-viewport-id');
        const url = `/dashboard/viewport/${user_id}/${viewport_id}`;
        window.open(url);
    });
});
