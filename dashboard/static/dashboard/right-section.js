const leftPanel = document.querySelector('#left-section');
const rightPanel = document.querySelector('#right-section');
const resizeHandle = document.querySelector('#resize-handle');
let initialX, initialLeftWidth, initialRightWidth;

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function setUserId(id) {
    user_id = id;
}
const viewportStreams = []; // list of livestreams currently in viewport

document.addEventListener('DOMContentLoaded', () => {
    const addButtons = document.querySelectorAll('.addview-btn');
    const resizePanelBtn = document.querySelector('#resize-panel-btn');
    const resizePanelTxt = document.querySelector('#resize-panel-txt');

    const saveViewportBtn = document.querySelector('#open-viewport-btn');
    saveViewportBtn.display = 'none';

    const quilt = document.querySelector('#quilt');

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

    /* Clicking the Save Viewport button opens a new tab with all streams currently in viewport */
    saveViewportBtn.addEventListener('click', () => {
        if (viewportStreams.length==0) {
            return;
        }

        const viewportName = document.querySelector('#viewport-name');
        // check if viewport name is valid
        if (!viewportName.value) {
            viewportName.classList.add("is-invalid");
            return;
        }

        // create a new json with fields user: user_id, livestreams: viewportStreams
        const data = {
            name: viewportName.value,
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

    /* Clicking the Clear button removes all streams from the viewport */
    const clearViewportBtn = document.querySelector('#clear-viewport-btn');
    clearViewportBtn.addEventListener('click', () => {
        displayContainers = document.querySelectorAll('.display-container');
        displayContainers.forEach((container) => {
            container.remove();
        });
        
        // for each stream in viewportStreams, display it in the left-section
        viewportStreams.forEach((streamId) => {
            const colparent = document.querySelector(`#col-${streamId}`);
            colparent.style.display = 'block';
        });
    });

    /* Listeners for switching between list view and grid view in viewport */
    const listviewBtn = document.querySelector('#list-view-btn');
    const gridviewBtn = document.querySelector('#grid-view-btn');
    listviewBtn.addEventListener('click', () => {
        // check if btn is active
        if (listviewBtn.classList.contains('active')) {
            return;
        } else {
            listviewBtn.classList.add('active');
            gridviewBtn.classList.remove('active');

            quilt.classList.remove('row-cols-2', 'row-cols-sm-2', 'row-cols-md-2', 'row-cols-lg-2', 'row-cols-xl-2', 'row-cols-xxl-2');
            quilt.classList.add('row-cols-1', 'row-cols-sm-1', 'row-cols-md-1', 'row-cols-lg-1', 'row-cols-xl-1', 'row-cols-xxl-1');
        }
    });
    gridviewBtn.addEventListener('click', () => {
        // check if btn is active
        if (gridviewBtn.classList.contains('active')) {
            return;
        } else {
            gridviewBtn.classList.add('active');
            listviewBtn.classList.remove('active');

            quilt.classList.remove('row-cols-1', 'row-cols-sm-1', 'row-cols-md-1', 'row-cols-lg-1', 'row-cols-xl-1', 'row-cols-xxl-1');
            quilt.classList.add('row-cols-2', 'row-cols-sm-2', 'row-cols-md-2', 'row-cols-lg-2', 'row-cols-xl-2', 'row-cols-xxl-2');
        }
    });

    /* Clicking an Add button adds the stream to the right-section's viewport 
     * and removes the item from the left-section's list of streams
    */
    addButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const buttonId = button.getAttribute('data-button-id');
            const image = document.querySelector(`#stream-${buttonId}`);
            const quilt = document.querySelector('#quilt');
            
            // save stream id to viewportStreams
            const id = image.getAttribute('data-id');
            viewportStreams.push(id);

            // check number of streams in viewport
            const numStreams = viewportStreams.length;
            if (numStreams == 1) {
                rightPanel.style.display = 'block';
            }

            // get the col div that the image is contained in, remove it
            const colparent = document.querySelector(`#col-${buttonId}`);
            colparent.style.display = 'none';

            /* Construct a new display-container in the following format:
            <div class="display-container col p-0">
              <div class="card">
                <a href="#" class="btn p-0" target="_blank" rel="noopener noreferrer" role="button">
                  <img class="card-img-top" data-id="{{ stream.id }}" src="https://cameras.alertcalifornia.org/public-camera-data/Axis-AlisoLaguna1/latest-frame.jpg?rqts=1683834051,Aliso" focusable="true" _mstaria-label="4468347" _mstHash="13" style="direction: ltr; text-align: left;"/>
                </a>
                <div class="card-body d-flex flex-column p-0">
                  <div class="display-info">
                    <div class="d-flex justify-content-between">
                      <p class="card-text">Laguna 1</p>
                      <p class="text-muted">CalFire</p>
                      <p class="text-muted">admin</p>
                      <div class="btn-group">
                        <button class="btn btn-sm btn-outline-danger">Remove</button>                   
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            */

            const colDiv = document.createElement('div');
            colDiv.classList.add('display-container', 'col', 'p-0');

            const cardDiv = document.createElement('div');
            cardDiv.classList.add('right-card', 'p-0');

            // create live-img and set src to the source of the stream with id == buttonId
            const liveImg = document.createElement('img');
            liveImg.classList.add('card-img-top');
            liveImg.src = image.getAttribute('data-source');
            liveImg.setAttribute('data-id', id);
            observer.observe(liveImg); // add observer to liveimg for periodic updates
            // add link to view stream in new window
            const alink = document.createElement('a');;
            alink.href = image.getAttribute('data-source');
            alink.target = '_blank';
            alink.rel = 'noopener noreferrer';
            alink.role = 'button';
            // put image inside the link
            alink.appendChild(liveImg);
            // add alink to cardDiv
            cardDiv.appendChild(alink);

            // create cardBodyDiv
            const cardBodyDiv = document.createElement('div');
            cardBodyDiv.classList.add('right-card-body', 'd-flex', 'flex-column', 'p-0');

            const displayInfo = document.createElement('div');
            displayInfo.classList.add('display-info');

            //create flexContainer
            const flexContainer = document.createElement('div');
            flexContainer.classList.add('d-flex', 'justify-content-between');
            
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
            flexContainer.appendChild(streamTitle);
            flexContainer.appendChild(streamAgency);
            flexContainer.appendChild(streamCreator);

            // create btn-group
            const btnGroup = document.createElement('div');
            btnGroup.classList.add('btn-group');
            const removeBtn = document.createElement('button');
            removeBtn.classList.add('btn', 'btn-sm', 'btn-outline-danger');
            removeBtn.innerHTML = 'Remove';
            btnGroup.appendChild(removeBtn);
            flexContainer.appendChild(btnGroup);

            removeBtn.addEventListener('click', () => {
                // remove display-container from quilt
                quilt.removeChild(colDiv);
                // remove stream id from viewportStreams
                const index = viewportStreams.indexOf(id);
                viewportStreams.splice(index, 1);
                // display the thumbnail in the left-section
                colparent.style.display = 'block';
            });
            
            displayInfo.appendChild(flexContainer);  
            cardBodyDiv.appendChild(displayInfo);
            cardDiv.appendChild(cardBodyDiv);
            colDiv.appendChild(cardDiv);         
            
            // add display-container to quilt
            quilt.insertBefore(colDiv, quilt.firstChild);
        });
    });
});
