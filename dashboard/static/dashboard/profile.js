
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

// uncheck private/public checkbox
function uncheckPrivatePublic(checkbox) {
    if (checkbox.checked) {
        // only get nongroupCheckboxes in the same form
        const form = checkbox.closest('form');
        const nongroupCheckboxes = form.querySelectorAll('input[type="checkbox"].nongroup');
        var classList = checkbox.classList;

        if (classList.contains('nongroup')) {
            // uncheck all other checkboxes
            var checkboxes = form.querySelectorAll('input[type="checkbox"]');
            for (var i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].id != checkbox.id){
                    checkboxes[i].checked = false;
                }
            }
        }
        else {
            // uncheck the nongroupCheckboxes
            for (var i = 0; i < nongroupCheckboxes.length; i++) {
                nongroupCheckboxes[i].checked = false;
            }
        }
    }
}
