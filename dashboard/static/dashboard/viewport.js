
document.addEventListener('DOMContentLoaded', () => {
    const listviewBtn = document.querySelector('#list-view-btn');
    const gridviewBtn = document.querySelector('#grid-view-btn');
    const rows = document.querySelectorAll('.rowdiv');

    listviewBtn.addEventListener('click', () => {
        listviewBtn.classList.add('active');
        gridviewBtn.classList.remove('active');
        rows.forEach(row => {
            row.classList.remove('row');
        });
    });

    gridviewBtn.addEventListener('click', () => {
        gridviewBtn.classList.add('active');
        listviewBtn.classList.remove('active');
        rows.forEach(row => {
            row.classList.add('row');
        });
    });

});