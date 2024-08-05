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
 * Learn more in https://angular.io/docs/ts/latest/guide/browser-support.html
 */

/**
 * By default, zone.js will patch all possible macroTask and DomEvents
 * user can disable parts of macroTask/DomEvents patch by setting following flags
 */
(window as any).__Zone_disable_requestAnimationFrame = true; // disable patch requestAnimationFrame
// (window as any).__Zone_disable_timers = true;
(window as any).__zone_symbol__BLACK_LISTED_EVENTS =
  ['scroll', 'mousemove', 'touchmove', 'touchend', 'touchstart', 'message', 'LIVE_SERVE_UPDATE']; // disable patch specified eventNames

(window as any).__Zone_ignore_on_properties =
  [{ target: WebSocket.prototype, ignoreProperties: ['close', 'error', 'open', 'message'] }];

/**
 * Zone JS is required by default for Angular itself.
 */
import 'zone.js/dist/zone-evergreen';  // Included with Angular CLI.

(window as any).global = window;

import * as smoothscroll from 'smoothscroll-polyfill';
// kick off the polyfill!
smoothscroll.polyfill();
