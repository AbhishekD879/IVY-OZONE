import 'ts-helpers';
import 'web-animations-js';
import '@angular/localize/init';

Error['stackTraceLimit'] = Infinity;
require('intersection-observer');

// Coral polyfills

// Used for reflect-metadata in JIT. If you use AOT (and only Angular decorators), you can remove.

// import 'web-animations-js';  // Run `npm install --save web-animations-js`.

/**
 * By default, zone.js will patch all possible macroTask and DomEvents
 * user can disable parts of macroTask/DomEvents patch by setting following flags
 */

(window as any).__Zone_disable_requestAnimationFrame = true; // disable patch requestAnimationFrame
// (window as any).__Zone_disable_on_property = true; // disable patch onProperty such as onclick
(window as any).__zone_symbol__BLACK_LISTED_EVENTS =
  ['scroll', 'touchstart', 'touchmove', 'touchend', 'message', 'LIVE_SERVE_UPDATE']; // disable patch specified eventNames
(window as any).__Zone_ignore_on_properties =
  [{ target: WebSocket.prototype, ignoreProperties: ['close', 'error', 'open', 'message'] }];

/**
 * in IE/Edge developer tools, the addEventListener will also be wrapped by zone.js
 * with the following flag, it will bypass `zone.js` patch for IE/Edge
 */
(window as any).__Zone_enable_cross_context_check = true;

import 'zone.js/dist/zone';
(window as any).global = window;

require('zone.js/dist/long-stack-trace-zone');
import * as smoothscroll from 'smoothscroll-polyfill';
// kick off the polyfill!
smoothscroll.polyfill();

/***************************************************************************************************
 * APPLICATION IMPORTS
 */

(function () {
  if ( typeof NodeList.prototype['forEach'] === 'function' ) { return false; }
  // @ts-ignore
   NodeList.prototype['forEach'] = Array.prototype.forEach;
})();
