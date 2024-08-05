var intervalId;
var isFast = true;
let cmsConfig;

onmessage = (message) => {
  cmsConfig = message.data;
  if (cmsConfig?.networkIndicatorEnabled) {
    checkNetworkConnectivity(cmsConfig);
  }
};

function checkNetworkConnectivity() {
  if (cmsConfig.debugLogEnabled) {
    console.log('*** Interval will create');
  }
  if (!intervalId) {
    intervalId = setInterval(() => {
      loaded = false;
      isSlow = setTimeout(() => {
        isFast = false;
        postMessage('slow');
  
      }, cmsConfig.slowTimeout);
  
      var startTime = new Date().getTime();
      var x = new XMLHttpRequest();
      x.responseType = "blob";
      x.onload = function () {
        var loadtime = new Date().getTime() - startTime;
        if (cmsConfig.debugLogEnabled) {
          console.log("**** Load Time");
          console.log(loadtime);
        }
        loaded = true;
        if (loadtime < cmsConfig.slowTimeout) {
          isFast = true;
          postMessage('online');
          if (cmsConfig.debugLogEnabled) {
            console.log("*** Net restored");
          }
        }
        clearTimeout(isSlow);
      };
      x.open("GET", cmsConfig.imageURL, true);
      x.setRequestHeader("Cache-Control", "no-cache, no-store, must-revalidate");
      x.setRequestHeader("Pragma", "no-cache");
      x.setRequestHeader("Expires", "0");
      if (cmsConfig.debugLogEnabled) {
        console.log(intervalId);
      }
      startTime = new Date().getTime();
      x.send();
    }, cmsConfig.pollingInterval);
  }
}

function clearIntervalForConnection() {
  clearInterval(intervalId);
}
