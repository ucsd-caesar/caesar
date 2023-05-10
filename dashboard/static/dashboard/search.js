const searchBtn = document.getElementById('search-btn');
const searchBar = document.getElementById('search-bar');
const searchForm = document.getElementById('search-form');

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
});

searchBtn.addEventListener('click', makeQuery);

// add event lister for pressing enter in search bar, then click search button
searchBar.addEventListener('keyup', (event) => {
    if (event.keyCode === 13) {
        event.preventDefault();
        searchBtn.click();
    }
});

function makeQuery() {
    let query = document.querySelector('input[type="search"]').value;
    fetch('/dashboard/search/?q=' + query)
    .then(response => response.json())
    .then(data => {
        let livestreamContainer = document.getElementById('livestream-container');
        livestreamContainer.innerHTML = '';
        
        data.forEach(stream => {
            let colDiv = document.createElement('div');
            colDiv.className = 'col';

            let cardDiv = document.createElement('div');
            cardDiv.className = 'card';
            colDiv.appendChild(cardDiv);

            let thumbnailUrl = stream.source.replace('latest-frame', 'latest-thumb');
            let aElement = document.createElement('a');
            aElement.href = stream.source;
            aElement.className = 'thumbnail-btn btn p-0';
            aElement.target = '_blank';
            aElement.rel = 'noopener noreferrer';
            cardDiv.appendChild(aElement);

            let imgElement = document.createElement('img');
            imgElement.id = 'stream-' + stream.id;
            imgElement.src = thumbnailUrl;
            imgElement.className = 'card-img-top';
            aElement.appendChild(imgElement);

            let cardBodyDiv = document.createElement('div');
            cardBodyDiv.className = 'card-body d-flex flex-column p-0';
            cardDiv.appendChild(cardBodyDiv);

            let cardBodyInnerDiv = document.createElement('div');
            cardBodyInnerDiv.className = 'd-flex align-items-center justify-content-start';
            cardBodyDiv.appendChild(cardBodyInnerDiv);

            let innerAElement = document.createElement('a');
            innerAElement.href = stream.source;
            innerAElement.className = 'btn pl-0 ml-0';
            innerAElement.target = '_blank';
            innerAElement.rel = 'noopener noreferrer';
            cardBodyInnerDiv.appendChild(innerAElement);

            let pElement = document.createElement('p');
            pElement.className = 'pl-0 ml-0';
            pElement.textContent = stream.title;
            innerAElement.appendChild(pElement);

            let secondDiv = document.createElement('div');
            secondDiv.className = 'd-flex align-items-center justify-content-between';
            cardBodyDiv.appendChild(secondDiv);

            let thirdDiv = document.createElement('div');
            secondDiv.appendChild(thirdDiv);

            let agencyAElement = document.createElement('a');
            agencyAElement.href = '/dashboard/agency/' + stream.agency.id;
            agencyAElement.className = 'btn pl-0 ml-0';
            agencyAElement.rel = 'noopener noreferrer';
            thirdDiv.appendChild(agencyAElement);

            let strongElement = document.createElement('strong');
            strongElement.className = 'text-muted';
            strongElement.textContent = stream.agency;
            agencyAElement.appendChild(strongElement);

            let fourthDiv = document.createElement('div');
            fourthDiv.className = 'float-end';
            secondDiv.appendChild(fourthDiv);

            let smallElement = document.createElement('small');
            smallElement.className = 'text-muted float-end';
            smallElement.innerHTML = stream.created_by;
            fourthDiv.appendChild(smallElement);

            let btnGroupDiv = document.createElement('div');
            btnGroupDiv.className = 'btn-group';
            cardBodyDiv.appendChild(btnGroupDiv);

            let buttonElement = document.createElement('button');
            buttonElement.className = 'addview-btn btn btn-sm btn-outline-primary';
            buttonElement.setAttribute('data-button-id', stream.id);
            buttonElement.textContent = 'Add to Viewport';
            btnGroupDiv.appendChild(buttonElement);

            livestreamContainer.appendChild(colDiv);
        });
    });
}


