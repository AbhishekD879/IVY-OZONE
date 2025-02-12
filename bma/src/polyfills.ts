/***************************************************************************************************
 * Load `$localize` onto the global scope - used if i18n tags appear in Angular templates.
 */
import '@angular/localize/init';
/**
 * This file includes polyfills needed by Angular and is loaded before the app.
 * You can add your own extra polyfills to this file.
 *
 * This file is divided into 2 sections:
 *   1. Browser polyfills. These are applied before loading ZoneJS and are sorted by browsers.
 *   2. Application imports. Files imported after ZoneJS that should be loaded before your main
 *      file.
 *
 * The current setup is for so-called "evergreen" browsers; the last versions of browsers that
 * automatically update themselves. This includes Safari >= 10, Chrome >= 55 (including Opera),
 * Edge >= 13 on the desktop, and iOS 10 and Chrome on mobile.
 *
 * Learn more in https://angular.io/guide/browser-support
 */

/***************************************************************************************************
* BROWSER POLYFILLS
*/

// Used for reflect-metadata in JIT. If you use AOT (and only Angular decorators), you can remove.
// import 'web-animations-js';  // Run `npm install --save web-animations-js`.

/**
 * By default, zone.js will patch all possible macroTask and DomEvents
 * user can disable parts of macroTask/DomEvents patch by setting following flags
 */
(window as any).__Zone_disable_requestAnimationFrame = true; // disable patch requestAnimationFrame
// (window as any).__Zone_disable_timers = true; // setTimeout/setInterval/setImmediate will be patched as Zone MacroTask
// (window as any).__Zone_disable_on_property = true; // disable patch onProperty such as onclick
(window as any).__zone_symbol__BLACK_LISTED_EVENTS =
  ['scroll', 'mousemove', 'touchmove', 'touchend', 'touchstart', 'message', 'LIVE_SERVE_UPDATE']; // disable patch specified eventNames

(window as any).__Zone_ignore_on_properties =
  [{ target: WebSocket.prototype, ignoreProperties: ['close', 'error', 'open', 'message'] }];
/**
 * in IE/Edge developer tools, the addEventListener will also be wrapped by zone.js
 * with the following flag, it will bypass `zone.js` patch for IE/Edge
 */
// (window as any).__Zone_enable_cross_context_check = true;

/**
 * Zone JS is required by default for Angular itself.
 */
 import 'zone.js/dist/zone';  // Included with Angular CLI.
(window as any).global = window;

import * as smoothscroll from 'smoothscroll-polyfill';
// kick off the polyfill!
smoothscroll.polyfill();
/**
 * APPLICATION IMPORTS
 */
(function () {
  if (typeof NodeList.prototype['forEach'] === 'function') {
    return false;
  }
  // @ts-ignore
 NodeList.prototype['forEach'] = Array.prototype.forEach;
})();

/**
 * 3.04kB gzip
 */
import 'whatwg-fetch';

import 'custom-event-polyfill';
