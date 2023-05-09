const leftPanel = document.querySelector('#left-section');
const rightPanel = document.querySelector('#right-section');
const resizeHandle = document.querySelector('#resize-handle');
let initialX, initialLeftWidth, initialRightWidth;

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function setUserId(id) {
    user_id = id;
}

document.addEventListener('DOMContentLoaded', () => {
    const addButtons = document.querySelectorAll('.addview-btn');
    const resizePanelBtn = document.querySelector('#resize-panel-btn');
    const resizePanelTxt = document.querySelector('#resize-panel-txt');

    const openViewportBtn = document.querySelector('#open-viewport-btn');

    const viewportStreams = []; // list of livestreams currently in viewport

    /* Clicking the Expand button expands the right-section to fill the viewport */
    resizePanelBtn.addEventListener('click', onExpandBtn);
    function onExpandBtn() {
        resizePanelBtn.addEventListener('click', onCollapseBtn);
        resizePanelBtn.removeEventListener('click', onExpandBtn);
        leftPanel.style.display = 'none';
        resizePanelTxt.innerHTML = 'Collapse Viewport';
        resizePanelTxt.classList.remove('float-start');
        resizePanelTxt.classList.add('float-end');
        rightPanel.style.width = '100%';
    }

    /* Clicking the Collapse button collapses the right-section to its original size */
    function onCollapseBtn() {
        resizePanelBtn.addEventListener('click', onExpandBtn);
        resizePanelBtn.removeEventListener('click', onCollapseBtn);
        leftPanel.style.display = 'block';
        resizePanelTxt.innerHTML = 'Expand Viewport';
        resizePanelTxt.classList.remove('float-end');
        resizePanelTxt.classList.add('float-start');
        // resize right-section to original width
        rightPanel.style.width = 'min(300vw, 1000px)';
    }


    /* Clicking the Open Viewport button opens a new tab with all streams currently in viewport */
    openViewportBtn.addEventListener('click', () => {
        // create a new json with fields user: user_id, livestreams: viewportStreams
        const data = {
            user: user_id,
            livestreams: viewportStreams
        };
        // send a POST request to /dashboard/viewport/post_viewport
        fetch('/dashboard/viewport/post_viewport/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(data),
        }).then((response) => response.json()).then(data =>{
            const viewport_id = data['id'];
            // open a new tab at user's most recent viewport
            const url = `/dashboard/viewport/${user_id}/${viewport_id}`;
            window.open(url);
        });
    });

    /* Clicking an Add button adds the stream to the right-section's viewport */
    addButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const buttonId = button.getAttribute('data-button-id');
            const image = document.querySelector(`#stream-${buttonId}`);
            const quilt = document.querySelector('#quilt');
            
            // save stream id to viewportStreams
            const id = image.getAttribute('data-id');
            viewportStreams.push(id);

            // create new display-img div and display-info div
            const displayImg = document.createElement('div');
            displayImg.classList.add('display-img');
            const displayInfo = document.createElement('div');
            displayInfo.classList.add('display-info');

            // create live-img and set src to the source of the stream with id == buttonId
            const liveImg = document.createElement('img');
            liveImg.classList.add('live-img');
            liveImg.src = image.getAttribute('data-source');
            // add link to view stream in new window
            const viewBtn = document.createElement('a');
            viewBtn.classList.add('thumbnail-btn', 'btn', 'p-0');
            viewBtn.href = image.getAttribute('data-source');
            viewBtn.target = '_blank';
            viewBtn.rel = 'noopener noreferrer';
            viewBtn.role = 'button';
            // put image inside the link
            viewBtn.appendChild(liveImg);
            // add image to display-img div
            displayImg.appendChild(viewBtn);

            // create div to hold stream info and a btn-group
            const infoContainer = document.createElement('div');
            infoContainer.classList.add('d-flex', 'justify-content-between', 'align-items-center');
            
            // create stream-title, stream-agency, stream-creator
            const streamTitle = document.createElement('p');
            streamTitle.classList.add('card-text');
            const streamAgency = document.createElement('p');
            streamAgency.classList.add('text-muted');
            const streamCreator = document.createElement('p');
            streamCreator.classList.add('text-muted');
            streamTitle.innerHTML = image.getAttribute('data-title');
            streamAgency.innerHTML = image.getAttribute('data-agency');
            streamCreator.innerHTML = image.getAttribute('data-creator');
            infoContainer.appendChild(streamTitle);
            infoContainer.appendChild(streamAgency);
            infoContainer.appendChild(streamCreator);

            // create btn-group
            const btnGroup = document.createElement('div');
            btnGroup.classList.add('btn-group');
            const removeBtn = document.createElement('button');
            removeBtn.classList.add('btn', 'btn-sm', 'btn-outline-danger');
            removeBtn.innerHTML = 'Remove';
            btnGroup.appendChild(removeBtn);
            infoContainer.appendChild(btnGroup);

            removeBtn.addEventListener('click', () => {
                // remove display-container from quilt
                quilt.removeChild(displayContainer);
                // remove stream id from viewportStreams
                const index = viewportStreams.indexOf(id);
                viewportStreams.splice(index, 1);
            });
            
            // add infoContainer to displayInfo
            displayInfo.appendChild(infoContainer);

            // add displayImg and displayInfo to a display-container div
            const displayContainer = document.createElement('div');
            displayContainer.classList.add('display-container', 'p-0', 'm-0');
            displayContainer.appendChild(displayImg);
            displayContainer.appendChild(displayInfo);
            
            // add display-container to quilt
            quilt.appendChild(displayContainer);
        });
    });
});
