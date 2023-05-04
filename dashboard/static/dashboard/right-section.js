const leftPanel = document.querySelector('#left-section');
const rightPanel = document.querySelector('#right-section');
const resizeHandle = document.querySelector('#resize-handle');
let initialX, initialLeftWidth, initialRightWidth;

resizeHandle.addEventListener('mousedown', (e) => {
    e.preventDefault();
    initialX = e.clientX;
    initialLeftWidth = leftPanel.getBoundingClientRect().width;
    initialRightWidth = rightPanel.getBoundingClientRect().width;
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
});

function onMouseMove(e) {
    const container = leftPanel.parentElement;
    const containerWidth = container.getBoundingClientRect().width;
    const newRightWidth = initialRightWidth - e.clientX + initialX;

    if (newRightWidth < containerWidth && newRightWidth > 0) {
    rightPanel.style.width = newRightWidth + 'px';
    leftPanel.style.width = containerWidth - newRightWidth + 'px';
    }
}

function onMouseUp() {
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
}