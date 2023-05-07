const leftPanel = document.querySelector('#left-section');
const rightPanel = document.querySelector('#right-section');
const resizeHandle = document.querySelector('#resize-handle');
let initialX, initialLeftWidth, initialRightWidth;

document.addEventListener('DOMContentLoaded', () => {
    const addButtons = document.querySelectorAll('.addview-btn');
    const expandPanelBtn = document.querySelector('#expand-panel-btn');

    /* Clicking the Expand button expands the right-section to fill the viewport */
    expandPanelBtn.addEventListener('click', onExpandBtn);
    function onExpandBtn() {
        expandPanelBtn.addEventListener('click', onCollapseBtn);
        expandPanelBtn.removeEventListener('click', onExpandBtn);
        leftPanel.style.display = 'none';
        expandPanelBtn.innerHTML = 'Collapse';
        // resize right-section to fill viewport
        rightPanel.style.width = '100%';
    }
    /* Clicking the Collapse button collapses the right-section to its original size */
    function onCollapseBtn() {
        expandPanelBtn.addEventListener('click', onExpandBtn);
        expandPanelBtn.removeEventListener('click', onCollapseBtn);
        leftPanel.style.display = 'block';
        expandPanelBtn.innerHTML = 'Expand';
        // resize right-section to original width
        rightPanel.style.width = 'min(300vw, 1000px)';
    }

    
    /* Clicking an Add button adds the stream to the right-section's viewport */
    addButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const buttonId = button.getAttribute('data-button-id');
            const image = document.querySelector(`#stream-${buttonId}`);
            const quilt = document.querySelector('#quilt');
            
            // create new display-img div and display-info div
            const displayImg = document.createElement('div');
            displayImg.classList.add('display-img');
            const displayInfo = document.createElement('div');
            displayInfo.classList.add('display-info');

            // create live-img and set src to the source of the stream with id == buttonId
            const liveImg = document.createElement('img');
            liveImg.classList.add('live-img');
            liveImg.src = image.getAttribute('data-source');
            // add live-img to display-img div
            displayImg.appendChild(liveImg);

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

            // create btn-group and view/remove buttons
            const btnGroup = document.createElement('div');
            btnGroup.classList.add('btn-group');
            const viewBtn = document.createElement('button')
            viewBtn.classList.add('btn', 'btn-sm', 'btn-outline-secondary');
            const removeBtn = document.createElement('button');
            removeBtn.classList.add('btn', 'btn-sm', 'btn-outline-danger');
            viewBtn.innerHTML = 'View';
            removeBtn.innerHTML = 'Remove';
            btnGroup.appendChild(viewBtn);
            btnGroup.appendChild(removeBtn);
            infoContainer.appendChild(btnGroup);

            // create listeners for view and remove buttons
            viewBtn.addEventListener('click', () => {
                // open new tab to liveimg.src
                window.open(liveImg.src);
            });
            removeBtn.addEventListener('click', () => {
                // remove display-container from quilt
                quilt.removeChild(displayContainer);
            });
            
            // add infoContainer to displayInfo
            displayInfo.appendChild(infoContainer);

            // add displayImg and displayInfo to a display-container div
            const displayContainer = document.createElement('div');
            displayContainer.classList.add('display-container');
            displayContainer.appendChild(displayImg);
            displayContainer.appendChild(displayInfo);
            
            // add display-container to quilt
            quilt.appendChild(displayContainer);
        });
    });
});

/* START RESIZE RIGHT-SECTION */
/*
resizeHandle.addEventListener('mousedown', (e) => {
    e.preventDefault();
    initialX = e.clientX;
    initialLeftWidth = leftPanel.getBoundingClientRect().width;
    initialRightWidth = rightPanel.getBoundingClientRect().width;
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
});
*/
function onMouseMove(e) {
    const container = leftPanel.parentElement;
    const containerWidth = container.getBoundingClientRect().width;
    const newRightWidth = initialRightWidth - e.clientX + initialX;

    if (newRightWidth < containerWidth && newRightWidth > 0) {
    rightPanel.style.width = newRightWidth + 'px';
    leftPanel.style.width = containerWidth - newRightWidth + 'px';
    }
}

/* END RESIZE RIGHT-SECTION */