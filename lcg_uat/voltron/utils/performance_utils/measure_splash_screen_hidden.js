performance.mark('selenium_accessible');
var config = { attributes: false, childList: true, characterData: false, attributeOldValue : false };
// create an observer instance
var observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    console.log(mutation);
    if (mutation.type === 'childList' && mutation.removedNodes[0].id === 'splash-screen') {
        performance.mark('splash_hidden');
    }
  });
});
var onElementReady = function($element) {
  return new Promise((resolve) => {
    var waitForElement = function() {
      if ($element) {
        resolve($element);
      } else {
        window.requestAnimationFrame(waitForElement);
      }
    };
    waitForElement();
  })
};

var $someElement = document.querySelector('[id="home-screen"]');
onElementReady($someElement)
  .then(() => {
    var splash = document.querySelector('[id="home-screen"]');
    observer.observe(splash, config);
  }
);
