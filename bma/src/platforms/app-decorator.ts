import { ApplicationRef, NgZone } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NavigationStart, NavigationEnd } from '@angular/router';

declare let window: any;

function decorateTick(appRef: ApplicationRef, ngZone: NgZone, pubSubService: PubSubService, router) {
  const debounceTime = 200;
  let callTimeout;
  let nextScheduled = false;

  // flag to control decorator to turn it Off in specific moments
  let isOff = false;

  // logic to Turn off tick decorator, as it affects angular material logic and login popup
  pubSubService.subscribe('tickDecorator', pubSubService.API.OPEN_LOGIN_DIALOG, () => { isOff = true; });
  pubSubService.subscribe('tickDecorator', pubSubService.API.LOGIN_DIALOG_CLOSED, () => { isOff = false; });
  pubSubService.subscribe('tickDecorator', pubSubService.API.VANILLA_SCOPE_CHANGE,
    (isVanillaPageOpened: boolean) => { isOff = isVanillaPageOpened; });

  // run native Tick function for route change logic
  router.events.subscribe(event => {
    if (event instanceof NavigationStart || event instanceof NavigationEnd) {
      // @ts-ignore
      appRef.tick(true);
    }
  });

  // global tick method to be decorated with debounce
  appRef.tick = (function(fn) {
    return function(callThrough?: boolean) {
      const self = this;

      if (!self._runningTick && (window.tickOff || isOff || callThrough)) {
        return ngZone.run(() => {
          fn.apply(self);
        });
      }

      if (callTimeout) {
        nextScheduled = true;
        return;
      }

      if (!self._runningTick) {
        // eslint-disable-next-line prefer-rest-params
        fn.apply(self, arguments);
      }

      ngZone.runOutsideAngular(() => {
        callTimeout = setTimeout(() => {
          callTimeout = null;

          if (nextScheduled && !self._runningTick) {
            // @ts-ignore
            // eslint-disable-next-line prefer-rest-params
            fn.apply(self, arguments);
            nextScheduled = false;
          }
        }, debounceTime);
      });
    };
  })(appRef.tick);
}

export default decorateTick;
