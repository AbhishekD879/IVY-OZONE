/* eslint-disable no-var, vars-on-top, prefer-arrow-callback, no-undef, consistent-return */

var timeTimeoutEvents = {},
  timeIntervalEvents = {},
  maxSlipTime = 2 * 1000; // 2 sec

function findTimeEvent(eventName) {
  return timeTimeoutEvents[eventName] !== undefined || timeIntervalEvents[eventName] !== undefined;
}

// Triggered by postMessage in the page
onmessage = function(evt) {
  // evt.data will be 0 here from the above postMessage

  if (evt.data.checkWorkerAvailability) {
    return postMessage({ checkWorkerAvailability: true });
  }

  if (evt.data.checkWorkerSync) {
    var startTime = Date.now();

    timeIntervalEvents.checkWorkerSync = {
      interval: setInterval(function() {
        startTime += evt.data.interval;
        var currentTime = Date.now();

        if (startTime < currentTime - maxSlipTime || startTime > currentTime + maxSlipTime) {
          postMessage({ checkWorkerSync: true });
        }

        startTime = currentTime;
      }, evt.data.interval)
    };

    return;
  }

  if (evt.data.clearTimeouts === true) {
    timeTimeoutEvents = {};
  }

  if (evt.data.clearIntervals === true) {
    timeIntervalEvents = {};
  }

  if (evt.data.type === 'interval' || evt.data.type === 'timeout') {
    if (findTimeEvent(evt.data.eventData.eventName)) {
      // Clear timeouts and intervals if repeated.
      if (evt.data.type === 'timeout') {
        clearTimeout(timeTimeoutEvents[evt.data.eventData.eventName].timeout);
        delete timeTimeoutEvents[evt.data.eventData.eventName];
      } else {
        clearInterval(timeIntervalEvents[evt.data.eventData.eventName].interval);
        delete timeIntervalEvents[evt.data.eventData.eventName];
      }
    }

    // Set timeouts and intervals.
    if (evt.data.type === 'timeout') {
      timeTimeoutEvents[evt.data.eventData.eventName] = {
        timeout: setTimeout(function() {
          postMessage(evt.data.eventData);
        }, evt.data.interval),
        eventData: evt.data.eventData
      };
    } else {
      timeIntervalEvents[evt.data.eventData.eventName] = {
        interval: setInterval(function() {
          postMessage(evt.data.eventData);
        }, evt.data.interval),
        eventData: evt.data.eventData
      };
    }
  }
};
