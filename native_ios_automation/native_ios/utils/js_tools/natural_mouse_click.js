var webElement = arguments[0]

function triggerMouseEvent (we, eventType) {
    var mouseEvent = document.createEvent('MouseEvents');
    mouseEvent.initEvent(eventType, true, true);
    we.dispatchEvent(mouseEvent);
}


['mouseover', 'mousedown', 'mouseup', 'click'].forEach(function(eventType) {
        triggerMouseEvent(webElement, eventType);
    });
