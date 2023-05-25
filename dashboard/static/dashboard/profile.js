
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

        const response = await fetch(`/dashboard/user/${livestreamId}/delete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: new URLSearchParams({livestream_id: livestreamId}),
        });

        const result = await response.json();
        if (result.status === 'success') {
            location.reload();
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

// add event listener for each delete button
const deleteBtns = document.querySelectorAll('.delete-viewport-btn');
deleteBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
        const viewport_id = btn.getAttribute('data-viewport-id');
        const response = await fetch(`/dashboard/viewport/${viewport_id}/delete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: new URLSearchParams({viewport_id: viewport_id}),
        });

        const result = await response.json();
        if (result.status === 'success') {
            location.reload();
        } else {
            console.error(result.message);
        }
    });
});

// uncheck other checkboxes
function uncheckOthers(checkbox) {
    if (checkbox.checked) {
        var value = checkbox.value;
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].value != value) {
                checkboxes[i].checked = false;
            }
        }
    }
}

// uncheck private/public checkbox
function uncheckPrivatePublic(checkbox) {
    if (checkbox.checked) {
        var value = checkbox.value;
        var checkboxes = document.getElementsByName('private_public');
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = false;
        }
    }
}

// add event listener for each form's submit button
/*
const submitBtns = document.querySelectorAll('.submit-btn');
submitBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
        livestream_id = btn.getAttribute('data-stream-id');

        const response = await fetch(`/dashboard/change-visibility/${livestream_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken,
            },
            body: new URLSearchParams({livestream_id: livestreamId}),
        });

        const result = await response.json();
        if (result.status === 'success') {
            location.reload();
        } else {
            console.error(result.message);
        }
    });
});
*/
