// This is the selector for the popup you want to delete.
const popupSelector = arguments[0]; // Change this to the actual selector for your popup.
(() => {
    let oldPushState = history.pushState;
    history.pushState = function pushState() {
        let ret = oldPushState.apply(this, arguments);
        window.dispatchEvent(new Event('pushstate'));
        window.dispatchEvent(new Event('locationchange'));
        return ret;
    };

    let oldReplaceState = history.replaceState;
    history.replaceState = function replaceState() {
        let ret = oldReplaceState.apply(this, arguments);
        window.dispatchEvent(new Event('replacestate'));
        window.dispatchEvent(new Event('locationchange'));
        return ret;
    };

    window.addEventListener('popstate', () => {
        window.dispatchEvent(new Event('locationchange'));
    });
})();
// Function to delete the popup.
function deletePopup() {
  console.log('Attempting to delete popup:', popupSelector);
  const popups = document.querySelectorAll(popupSelector);
  popups.forEach((popup) => {
    if (popup && typeof popup.remove === 'function') {
        popup.remove(); // This will delete the popup element from the DOM.
        console.log('Popup deleted:', popupSelector);
    } else if (popup && popup.parentNode) {
        // Fallback for older browsers.
        popup.parentNode.removeChild(popup);
        console.log('Popup removed via parentNode:', popupSelector);
    }
 })


}

// Create an observer instance linked to a callback function.
const observer = new MutationObserver((mutationsList, observer) => {
 console.log('Added nodes:', mutationsList);
  for (let mutation of mutationsList) {
    if (mutation.type === 'childList') {
      const addedNodes = [...mutation.addedNodes];
      console.log('Added nodes:', addedNodes)
      const popup = addedNodes.find(node => node.matches && node.matches(popupSelector));
      if (popup) {
        deletePopup();
        // Optional: Disconnect the observer if it's no longer needed.
        // observer.disconnect();
      }
    }
  }
});

// Start observing the document body for DOM mutations.
observer.observe(document.body, { attributes: false, childList: true, subtree: true });
window.addEventListener('locationchange',deletePopup)
window.addEventListener('load', deletePopup);
// Handle the case where the popup might be present from the start.
deletePopup();
